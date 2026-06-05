
import ipaddress
import os
import sqlite3
import subprocess
from pathlib import Path


DB_PATH = "demo.db"
EXPORT_ROOT = Path("./exports").resolve()


def find_user_by_name(username: str):
    """
    Fix: use parameterized SQL instead of string concatenation.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, role FROM users WHERE username = ?",
            (username,),
        )
        return cursor.fetchall()
    finally:
        conn.close()


def export_file(filename: str) -> str:
    """
    Fix: resolve the requested path and ensure it stays inside EXPORT_ROOT.
    """
    candidate = (EXPORT_ROOT / filename).resolve()

    try:
        candidate.relative_to(EXPORT_ROOT)
    except ValueError as exc:
        raise ValueError("invalid export path") from exc

    if not candidate.is_file():
        raise FileNotFoundError(filename)

    return candidate.read_text(encoding="utf-8")


def ping_host(host: str) -> str:
    """
    Fix: validate the host and avoid shell=True.
    """
    ipaddress.ip_address(host)

    return subprocess.check_output(
        ["ping", "-c", "1", host],
        text=True,
    )


def is_admin(token: str) -> bool:
    """
    Fix: read the expected admin token from environment instead of hardcoding it.
    """
    expected_token = os.getenv("ADMIN_TOKEN")
    if not expected_token:
        return False

    return token == expected_token


if __name__ == "__main__":
    print(find_user_by_name("alice"))
    print(export_file("report.txt"))
    print(ping_host("127.0.0.1"))
    print(is_admin(os.getenv("ADMIN_TOKEN", "")))
