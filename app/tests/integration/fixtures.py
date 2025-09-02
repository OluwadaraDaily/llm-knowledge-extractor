"""Shared fixtures for integration tests."""

import pytest
import tempfile
import os
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from app.db.models import Analysis
from app.db.migrator import run_migrations, drop_tables


@pytest.fixture
def client():
    """Create FastAPI test client."""
    return TestClient(app)


@pytest.fixture
async def test_db():
    """Setup and teardown isolated test database for each test."""
    # Create a temporary database file for this test
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp_file:
        test_db_path = tmp_file.name
    
    # Patch the DB_PATH to use our test database
    with patch('app.db.connection.DB_PATH', test_db_path):
        # Setup: Create test database
        await run_migrations()
        yield
        # Teardown: Clean up test database
        await drop_tables()
    
    # Remove the temporary database file
    if os.path.exists(test_db_path):
        os.unlink(test_db_path)


@pytest.fixture(scope="module", autouse=True)
async def setup_test_db():
    """Setup test database once for all tests in a module."""
    await run_migrations()


@pytest.fixture
async def sample_data(test_db):
    """Create sample analysis data for testing search endpoints."""
    sample_analyses = [
        Analysis(
            input_text="Python is an excellent programming language for data science and web development.",
            summary="Discussion about Python programming language capabilities",
            title="Python Programming Guide",
            topics=["python", "programming", "data science", "web development"],
            sentiment="positive",
            keywords=["python", "programming", "language"]
        ),
        Analysis(
            input_text="JavaScript frameworks are becoming increasingly complex and difficult to learn.",
            summary="Critical view of modern JavaScript development complexity",
            title="JavaScript Complexity Issues",
            topics=["javascript", "frameworks", "web development"],
            sentiment="negative",
            keywords=["javascript", "frameworks", "complex"]
        ),
        Analysis(
            input_text="Machine learning algorithms require substantial computational resources and data.",
            summary="Overview of machine learning requirements",
            title="ML Resource Requirements",
            topics=["machine learning", "algorithms", "data", "computing"],
            sentiment="neutral",
            keywords=["machine", "learning", "algorithms"]
        ),
        Analysis(
            input_text="The new database management system offers improved performance and reliability.",
            summary="Review of new database system features",
            title="Database System Review",
            topics=["database", "performance", "reliability"],
            sentiment="positive",
            keywords=["database", "system", "performance"]
        ),
        Analysis(
            input_text="Cloud computing services are revolutionizing how businesses operate and scale.",
            summary="Impact of cloud computing on business operations",
            title="Cloud Computing Revolution",
            topics=["cloud computing", "business", "scaling"],
            sentiment="positive",
            keywords=["cloud", "computing", "business"]
        )
    ]
    
    # Save all sample analyses
    for analysis in sample_analyses:
        await analysis.save()
    
    return sample_analyses