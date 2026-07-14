import sys
import os

sys.path.append(os.path.dirname(__file__))

from app.database import engine
from sqlalchemy import text


def run_migration():
    with engine.connect() as conn:
        try:
            conn.execute(
                text("ALTER TABLE submissions ADD COLUMN github_url VARCHAR(255);")
            )
            print("Added github_url column")
        except Exception as e:
            print(f"Error adding github_url: {e}")

        try:
            conn.execute(text("ALTER TABLE submissions MODIFY code_snippet LONGTEXT;"))
            print("Modified code_snippet to LONGTEXT")
        except Exception as e:
            print(f"Error modifying code_snippet: {e}")

        try:
            conn.execute(
                text("ALTER TABLE submissions MODIFY code_snippet LONGTEXT NULL;")
            )
            print("Modified code_snippet to LONGTEXT NULL")
        except Exception as e:
            print(f"Error modifying code_snippet NULL: {e}")

        conn.commit()


if __name__ == "__main__":
    run_migration()
