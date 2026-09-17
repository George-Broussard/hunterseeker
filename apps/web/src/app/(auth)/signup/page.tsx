import type { Metadata } from "next";

import { SignupForm } from "./signup-form";

export const metadata: Metadata = { title: "Create an account — hunter/seeker" };

export default function SignupPage() {
  return <SignupForm />;
}
