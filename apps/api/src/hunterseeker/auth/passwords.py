"""Password hashing with argon2id (``argon2-cffi``).

Hashing is CPU-bound by design; call the async wrappers from request handlers so the event
loop stays free (AGENTS.md §8).
"""

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from starlette.concurrency import run_in_threadpool

_hasher = PasswordHasher()

# A real hash of a random password, verified against when the account does not exist so a
# failed login costs the same time either way (no account enumeration via timing).
_DUMMY_HASH = _hasher.hash("hunterseeker-dummy-password-for-timing-equalisation")


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password: str, password_hash: str | None) -> bool:
    """True iff ``password`` matches ``password_hash``. ``None`` always verifies false."""
    try:
        return _hasher.verify(password_hash or _DUMMY_HASH, password) and password_hash is not None
    except VerifyMismatchError, VerificationError, InvalidHashError:
        return False


async def hash_password_async(password: str) -> str:
    return await run_in_threadpool(hash_password, password)


async def verify_password_async(password: str, password_hash: str | None) -> bool:
    return await run_in_threadpool(verify_password, password, password_hash)
