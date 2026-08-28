import hashlib
import os
import re
import secrets

import streamlit as st

from database.connection import get_connection


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return salt.hex() + ":" + dk.hex()


def verify_password(password: str, stored: str) -> bool:
    try:
        salt_hex, dk_hex = stored.split(":")
        salt = bytes.fromhex(salt_hex)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
        return dk.hex() == dk_hex
    except Exception:
        return False


def is_valid_email(email: str) -> bool:
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email or "") is not None


def _issue_token(user_id):
    token = secrets.token_hex(16)
    conn = get_connection()
    conn.execute("UPDATE users SET token = ? WHERE id = ?", (token, user_id))
    conn.commit()
    conn.close()
    return token


def _sync_url(token):
    if token and st.query_params.get("t") != token:
        st.query_params["t"] = token


def register_user(email, password, password2):
    email = (email or "").strip().lower()
    if not is_valid_email(email):
        return False, "Некорректный email"
    if len(password or "") < 6:
        return False, "Пароль должен быть не короче 6 символов"
    if password != password2:
        return False, "Пароли не совпадают"

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, hash_password(password)),
        )
        conn.commit()
        user_id = cur.lastrowid
    except Exception:
        conn.close()
        return False, "Пользователь с таким email уже существует"
    conn.close()

    st.session_state["user_id"] = user_id
    _sync_url(_issue_token(user_id))
    return True, "Аккаунт создан!"


def login_user(email, password):
    email = (email or "").strip().lower()
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if row is None or not verify_password(password, row["password_hash"]):
        return False, "Неверный email или пароль"

    st.session_state["user_id"] = row["id"]
    _sync_url(_issue_token(row["id"]))
    return True, "Добро пожаловать!"


def logout_user():
    st.session_state.pop("user_id", None)
    st.query_params.clear()


def get_session_user():
    user_id = st.session_state.get("user_id")
    if not user_id:
        return None
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_current_user():
    user_id = st.session_state.get("user_id")
    if not user_id:
        token = st.query_params.get("t")
        if token:
            conn = get_connection()
            row = conn.execute("SELECT * FROM users WHERE token = ?", (token,)).fetchone()
            conn.close()
            if row:
                user_id = row["id"]
                st.session_state["user_id"] = user_id
    if not user_id:
        return None

    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if row is None:
        st.session_state.pop("user_id", None)
        return None
    _sync_url(row["token"])
    return dict(row)