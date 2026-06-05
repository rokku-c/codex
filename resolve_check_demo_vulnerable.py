from __future__ import annotations

  import re
  import sqlite3
  import subprocess
  from pathlib import Path

  DB_PATH = Path("demo_users.db")


  def find_user_by_name(username: str) -> list[tuple[int, str, str]]:
      with sqlite3.connect(DB_PATH) as conn:
          cursor = conn.cursor()
          query = "SELECT id, username, role FROM users WHERE username = ?"
          return cursor.fetchall()


  def ping_host(host: str) -> str:
      if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", host):
          raise ValueError(f"Invalid host: {host}")
      return subprocess.check_output(["ping", "-c", "1", host], text=True)


  if __name__ == "__main__":
      print(find_user_by_name("alice"))
      print(ping_host("127.0.0.1"))
