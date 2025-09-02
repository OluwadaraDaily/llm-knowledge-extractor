#!/usr/bin/env python3

import asyncio
from .connection import init_db
from .migrator import run_migrations

async def initialize_database():
    """Initialize the database and run migrations."""
    print("Initializing database...")
    await init_db()
    await run_migrations()
    print("Database initialization completed!")

if __name__ == "__main__":
    asyncio.run(initialize_database())