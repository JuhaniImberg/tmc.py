import sqlite3
import os


class DB:

    """Our configuration manager."""

    def __init__(self):
        self.conn = sqlite3.connect(
            os.path.join(os.path.expanduser("~"), '.config', 'tmc.db'))
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self.create_tables()

    def reset(self):
        self.c.execute("DROP TABLE IF EXISTS courses")
        self.c.execute("DROP TABLE IF EXISTS exercises")
        self.c.execute("DROP TABLE IF EXISTS config")
        self.create_tables()

    def create_tables(self):
        self.c.execute("""  CREATE TABLE IF NOT EXISTS courses (
                                id          INTEGER PRIMARY KEY     NOT NULL,
                                name        TEXT                    NOT NULL,
                                selected    INTEGER                 DEFAULT 0,
                                path        TEXT                    DEFAULT ""
                            )""")

        self.c.execute("""  CREATE TABLE IF NOT EXISTS exercises (
                                id          INTEGER PRIMARY KEY     NOT NULL,
                                name        TEXT                    NOT NULL,
                                course_id   INTEGER                 NOT NULL,
                                selected    INTEGER                 DEFAULT 0,
                                downloaded  INTEGER                 DEFAULT 0,
                                attempted   INTEGER                 DEFAULT 0,
                                completed   INTEGER                 DEFAULT 0
                            )""")

        self.c.execute("""  CREATE TABLE IF NOT EXISTS config (
                                name        TEXT PRIMARY KEY        NOT NULL,
                                value       TEXT                    NOT NULL
                            )""")

        self.conn.commit()

    # config stuff

    def config_set(self, name, value):
        self.c.execute("""  INSERT OR REPLACE INTO config (name, value)
                            VALUES (?, ?)""", (name, value,))
        self.conn.commit()

    def config_get(self, name):
        self.c.execute("SELECT * FROM config WHERE name=?", (name,))
        row = self.c.fetchone()
        if row == None:
            raise Exception("Key not found!")
        return row["value"]

    # course stuff

    def add_course(self, course):
        self.c.execute("""  INSERT OR IGNORE INTO courses (id, name)
                            VALUES (?, ?)""", (course["id"], course["name"]))
        self.conn.commit()

    def get_courses(self):
        self.c.execute("SELECT * FROM courses")
        return self.c.fetchall()

    def select_course(self, id):
        self.c.execute("UPDATE courses SET selected=0")
        self.c.execute("UPDATE courses SET selected=1 WHERE id=?", (id,))
        self.conn.commit()

    def set_selected_path(self, path):
        self.c.execute("UPDATE courses SET path=? WHERE selected=1", (path,))
        self.conn.commit()

    def selected_course(self):
        self.c.execute("SELECT * FROM courses WHERE selected = 1")
        return self.c.fetchone()

    # exercise stuff

    def add_exercise(self, exercise, course):
        self.c.execute("""  INSERT OR IGNORE INTO exercises (
                            id, name, course_id, attempted, completed)
                            VALUES (?, ?, ?, ?, ?)""", (exercise["id"],
                                                        exercise["name"],
                                                        course["id"],
                                                        exercise["attempted"],
                                                        exercise["completed"],))
        self.conn.commit()

    def get_exercises(self):
        self.c.execute("SELECT * FROM exercises")
        return self.c.fetchall()

    def select_exercise(self, id):
        self.c.execute("UPDATE exercises SET selected=0")
        self.c.execute("UPDATE exercises SET selected=1 WHERE id=?", (id,))
        self.conn.commit()

    def selected_exercise(self):
        self.c.execute("SELECT * FROM exercises WHERE selected = 1")
        return self.c.fetchone()
