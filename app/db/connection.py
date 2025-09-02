import aiosqlite
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'knowledge.db')

@asynccontextmanager
async def get_db_connection() -> AsyncGenerator[aiosqlite.Connection, None]:
    """Async context manager for database connections."""
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        try:
            yield conn
            await conn.commit()
        except Exception:
            await conn.rollback()
            raise

async def init_db():
    """Initialize the database by creating the knowledge.db file if it doesn't exist."""
    if not os.path.exists(DB_PATH):
        async with get_db_connection() as conn:
            # verify DB is working
            await conn.execute("SELECT 1")
        print(f"Database created at: {DB_PATH}")
    else:
        print(f"Database already exists at: {DB_PATH}")