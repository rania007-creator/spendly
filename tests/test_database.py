import os
import pathlib
import sqlite3
import pytest
from app import app
from database.db import get_db, init_db

@pytest.fixture
def db(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("data") / "app.db"
    os.environ["DATABASE"] = str(db_path)
    with app.app_context():
        init_db()
        db_conn = get_db()
        yield db_conn
        db_conn.close()

def test_tables_exist(db):
    cursor = db.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    tables = {row["name"] for row in cursor}
    assert {"users", "categories", "expenses"} <= tables
