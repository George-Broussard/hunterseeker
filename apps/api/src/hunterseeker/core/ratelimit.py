"""In-process rate limiting: a fixed-window counter per key.

Held in ``app.state.rate_limiter`` (see ``core/app.py``), so it is scoped to one API
process — and, in tests, to one ``create_app()`` call, which keeps tests isolated from
each other without any explicit reset. Not safe across multiple replicas: the moment
this service runs more than one, swap ``InMemoryRateLimiter`` for a Redis-backed
implementation behind the same ``RateLimiter`` protocol (``INCR`` + ``EXPIRE``, or a Lua
script for atomicity across the check-and-increment). Nothing that calls ``allowed()`` /
``record()`` needs to change.
"""

import time
from dataclasses import dataclass, field
from threading import Lock
from typing import Protocol

from fastapi import Request


class RateLimiter(Protocol):
    def allowed(self, key: str, *, limit: int, window_seconds: float) -> bool:
        """True if ``key`` has recorded fewer than ``limit`` occurrences in the trailing
        ``window_seconds``. Does not itself record an occurrence — call ``record`` for
        that once the caller has decided the attempt counts against the budget."""
        ...

    def record(self, key: str, *, window_seconds: float) -> None:
        """Record one occurrence of ``key``, starting a fresh window if the previous one
        has expired."""
        ...


@dataclass
class InMemoryRateLimiter:
    """Fixed-window counter per key, held in process memory.

    A fixed (not sliding) window can admit up to ``2 * limit`` occurrences across a
    window boundary in the worst case. That's an acceptable trade for the simplicity of
    "for now, in-process" (issue #24); revisit if it proves too permissive once this
    moves to a shared Redis-backed limiter.
    """

    _windows: dict[str, tuple[float, int]] = field(default_factory=dict)
    _lock: Lock = field(default_factory=Lock)

    def allowed(self, key: str, *, limit: int, window_seconds: float) -> bool:
        with self._lock:
            return self._count(key, window_seconds) < limit

    def record(self, key: str, *, window_seconds: float) -> None:
        now = time.monotonic()
        with self._lock:
            window_start, count = self._windows.get(key, (now, 0))
            if now - window_start >= window_seconds:
                window_start, count = now, 0
            self._windows[key] = (window_start, count + 1)

    def _count(self, key: str, window_seconds: float) -> int:
        window_start, count = self._windows.get(key, (time.monotonic(), 0))
        if time.monotonic() - window_start >= window_seconds:
            return 0
        return count


def get_rate_limiter(request: Request) -> RateLimiter:
    """The rate limiter for this app instance (``app.state.rate_limiter``)."""
    limiter: RateLimiter = request.app.state.rate_limiter
    return limiter


def client_ip(request: Request) -> str:
    """Best-effort caller IP.

    No trusted-proxy header parsing yet (``X-Forwarded-For`` et al.) — add it, reading
    only the hop nearest a trusted proxy, when this service sits behind a load balancer.
    Until then a shared NAT or a proxy in front of it makes this coarser than a true
    per-caller limit; the per-email limit on ``/verify`` doesn't depend on it.
    """
    return request.client.host if request.client else "unknown"
