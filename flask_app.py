import os
import sqlite3

from flask import Flask, abort, request

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "streak.db")


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS streak_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                current_streak INTEGER NOT NULL DEFAULT 0,
                patch_pb INTEGER NOT NULL DEFAULT 0,
                previous_pb INTEGER NOT NULL DEFAULT 0,
                last_title TEXT NOT NULL DEFAULT 'Dread'
            )
        """)

        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(streak_state)")
        }
        if "last_title" not in columns:
            connection.execute(
                "ALTER TABLE streak_state ADD COLUMN last_title TEXT NOT NULL DEFAULT 'Dread'"
            )

        connection.execute(
            "INSERT OR IGNORE INTO streak_state "
            "(id, current_streak, patch_pb, previous_pb, last_title) "
            "VALUES (1, 0, 0, 0, 'Dread')"
        )


init_db()


@app.route("/lati")
def lati_command():
    user = request.args.get("user", "Аноним")
    nick = user.lower().strip()

    if nick != "laatteeeee_":
        return "Ты не Лати -_-"

    real_name = "Лати"
    fake_name = "Светочка"

    if os.urandom(1)[0] % 2:
        real_name, fake_name = fake_name, real_name

    return f"Привет, {real_name}! Мы помним, что ты не {fake_name}"


@app.route("/str")
def streak_command():
    streak_value = request.args.get("streak", request.args.get("str"))

    try:
        streak = int(streak_value)
    except (TypeError, ValueError):
        return "Некорректный стрик", 400

    if streak < 0:
        return "Стрик не может быть отрицательным", 400

    with get_db() as connection:
        row = connection.execute(
            "SELECT patch_pb, previous_pb, last_title "
            "FROM streak_state WHERE id = 1"
        ).fetchone()

        title = request.args.get("title")
        if title is None:
            title = row["last_title"]
        else:
            title = title.strip() or row["last_title"]

        patch_pb = max(row["patch_pb"], streak)

        connection.execute(
            """
            UPDATE streak_state
            SET current_streak = ?, patch_pb = ?, last_title = ?
            WHERE id = 1
            """,
            (streak, patch_pb, title),
        )

        previous_pb = row["previous_pb"]

    return f"{title}. Streak: {streak} | PB - {patch_pb} | PB (Previous patches) - {previous_pb}"


@app.route("/str/reset", methods=["POST"])
def reset_streak():
    reset_key = os.environ.get("STR_RESET_KEY")
    supplied_key = request.args.get("key", request.headers.get("X-Reset-Key", ""))

    if not reset_key or supplied_key != reset_key:
        abort(403)

    with get_db() as connection:
        row = connection.execute(
            "SELECT patch_pb, previous_pb FROM streak_state WHERE id = 1"
        ).fetchone()

        previous_pb = max(row["previous_pb"], row["patch_pb"])
        connection.execute(
            """
            UPDATE streak_state
            SET current_streak = 0, patch_pb = 0, previous_pb = ?
            WHERE id = 1
            """,
            (previous_pb,),
        )

    return "Текущий патч сброшен"
