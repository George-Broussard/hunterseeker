"""Auth domain: the ``users`` table, signup / credential verification, and the JWT dependency.

Sessions live in ``apps/web`` (Auth.js). This package is what the web app calls to create a
user and to check a password, plus ``get_current_user`` — the dependency every other domain
uses to learn who is calling and which persona they are (AGENTS.md §4, decided in #3).
"""
