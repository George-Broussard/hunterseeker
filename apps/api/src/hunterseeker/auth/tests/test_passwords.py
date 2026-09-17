from hunterseeker.auth.passwords import hash_password, verify_password


def test_hash_verifies_and_is_salted() -> None:
    a = hash_password("correct horse battery staple")
    b = hash_password("correct horse battery staple")

    assert a != b
    assert a.startswith("$argon2id$")
    assert verify_password("correct horse battery staple", a)
    assert not verify_password("wrong", a)


def test_missing_hash_never_verifies() -> None:
    assert not verify_password("anything", None)
    assert not verify_password("hunterseeker-dummy-password-for-timing-equalisation", None)


def test_garbage_hash_never_verifies() -> None:
    assert not verify_password("anything", "not-a-phc-string")
