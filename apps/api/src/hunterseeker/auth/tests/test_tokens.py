import uuid
from datetime import timedelta

import jwt
import pytest

from hunterseeker.auth.tokens import (
    ALGORITHM,
    AUDIENCE,
    ISSUER,
    CurrentUser,
    InvalidTokenError,
    decode_api_token,
    encode_api_token,
)

SECRET = "test-secret-with-at-least-thirty-two-bytes"
USER = CurrentUser(id=uuid.uuid4(), role="hunter", email="h@example.com")


def test_round_trip() -> None:
    token = encode_api_token(USER, SECRET)

    assert decode_api_token(token, SECRET) == USER


def test_wrong_secret_rejected() -> None:
    token = encode_api_token(USER, SECRET)

    with pytest.raises(InvalidTokenError):
        decode_api_token(token, "other-secret-with-at-least-thirty-two-bytes")


def test_expired_rejected() -> None:
    token = encode_api_token(USER, SECRET, ttl=timedelta(seconds=-5))

    with pytest.raises(InvalidTokenError):
        decode_api_token(token, SECRET)


def test_wrong_audience_or_issuer_rejected() -> None:
    base = {"sub": str(USER.id), "role": "hunter", "iat": 0, "exp": 2**31}
    for override in ({"aud": "someone-else", "iss": ISSUER}, {"aud": AUDIENCE, "iss": "x"}):
        token = jwt.encode({**base, **override}, SECRET, algorithm=ALGORITHM)
        with pytest.raises(InvalidTokenError):
            decode_api_token(token, SECRET)


def test_unknown_role_rejected() -> None:
    claims = {
        "sub": str(USER.id),
        "role": "admin",
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": 0,
        "exp": 2**31,
    }
    token = jwt.encode(claims, SECRET, algorithm=ALGORITHM)

    with pytest.raises(InvalidTokenError, match="role"):
        decode_api_token(token, SECRET)


def test_alg_none_rejected() -> None:
    token = jwt.encode({"sub": str(USER.id), "role": "hunter"}, None, algorithm="none")

    with pytest.raises(InvalidTokenError):
        decode_api_token(token, SECRET)
