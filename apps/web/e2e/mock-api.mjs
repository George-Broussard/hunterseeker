// In-memory stand-in for apps/api's /api/v1/auth endpoints, for running the web e2e
// without Python + Postgres. Mirrors the contract in apps/api/src/hunterseeker/auth.
// Usage: node e2e/mock-api.mjs <port>
import { createHmac, randomUUID, timingSafeEqual } from "node:crypto";
import { createServer } from "node:http";

const port = Number(process.argv[2] ?? 8007);
const secret = process.env.AUTH_SECRET ?? "";
const users = new Map(); // email -> { id, email, name, role, password }
const ROLES = new Set(["hunter", "seeker"]);

function send(res, status, body) {
  res.writeHead(status, { "content-type": "application/json" });
  res.end(JSON.stringify(body));
}

function publicUser({ id, email, name, role }) {
  return { id, email, name, role };
}

/** Verify the HS256 bearer token the web app mints (see src/lib/auth/api-token.ts). */
function currentUser(req) {
  const [scheme, token] = (req.headers.authorization ?? "").split(" ");
  if (scheme !== "Bearer" || !token) return null;
  const [header, payload, signature] = token.split(".");
  if (!header || !payload || !signature) return null;
  const expected = createHmac("sha256", secret).update(`${header}.${payload}`).digest();
  const actual = Buffer.from(signature, "base64url");
  if (expected.length !== actual.length || !timingSafeEqual(expected, actual)) return null;
  const claims = JSON.parse(Buffer.from(payload, "base64url").toString());
  const now = Math.floor(Date.now() / 1000);
  if (claims.iss !== "hunterseeker-web" || claims.aud !== "hunterseeker-api") return null;
  if (typeof claims.exp !== "number" || claims.exp < now || !ROLES.has(claims.role)) return null;
  return { id: claims.sub, role: claims.role, email: claims.email ?? "" };
}

async function readJson(req) {
  let raw = "";
  for await (const chunk of req) raw += chunk;
  return raw ? JSON.parse(raw) : {};
}

createServer(async (req, res) => {
  if (req.method === "GET" && req.url === "/health") return send(res, 200, { status: "ok" });
  if (req.method === "GET" && req.url === "/api/v1/auth/me") {
    const user = currentUser(req);
    return user ? send(res, 200, user) : send(res, 401, { detail: "Not authenticated" });
  }
  if (req.method !== "POST") return send(res, 404, { detail: "Not Found" });
  const body = await readJson(req);
  const email = String(body.email ?? "")
    .trim()
    .toLowerCase();

  if (req.url === "/api/v1/auth/signup") {
    const { password, name, role } = body;
    const valid =
      email.includes("@") &&
      typeof password === "string" &&
      password.length >= 8 &&
      typeof name === "string" &&
      name.trim() &&
      ROLES.has(role);
    if (!valid) return send(res, 422, { detail: [{ msg: "invalid" }] });
    if (users.has(email)) {
      return send(res, 409, { detail: "An account with this email already exists" });
    }
    const user = { id: randomUUID(), email, name: name.trim(), role, password };
    users.set(email, user);
    return send(res, 201, publicUser(user));
  }

  if (req.url === "/api/v1/auth/verify") {
    const user = users.get(email);
    if (!user || user.password !== body.password) {
      return send(res, 401, { detail: "Invalid email or password" });
    }
    return send(res, 200, publicUser(user));
  }

  return send(res, 404, { detail: "Not Found" });
}).listen(port, () => console.log(`mock auth api on http://localhost:${port}`));
