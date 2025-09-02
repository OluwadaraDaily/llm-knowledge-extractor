from .connection import get_db_connection

async def run_migrations():
    """Run all database migrations."""
    async with get_db_connection() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT NOT NULL,
                summary TEXT,
                title TEXT,
                topics TEXT,
                sentiment TEXT,
                keywords TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    print("Database migrations completed successfully")

async def drop_tables():
    """Drop all tables (for development/testing)."""
    async with get_db_connection() as conn:
        await conn.execute("DROP TABLE IF EXISTS analyses")
    print("All tables dropped successfully")