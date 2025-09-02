import json
from typing import List
from .connection import get_db_connection

class Analysis:
    def __init__(self, input_text: str, summary: str = "", title: str = "", 
                 topics: List[str] = None, sentiment: str = "", keywords: List[str] = None):
        self.input_text = input_text
        self.summary = summary
        self.title = title
        self.topics = topics or []
        self.sentiment = sentiment
        self.keywords = keywords or []
    
    async def save(self) -> int:
        """Save the analysis to the database."""
        topics_str = json.dumps(self.topics) if self.topics else ""
        keywords_str = json.dumps(self.keywords) if self.keywords else ""
        
        async with get_db_connection() as conn:
            cursor = await conn.execute("""
                INSERT INTO analyses (input_text, summary, title, topics, sentiment, keywords)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.input_text, self.summary, self.title, topics_str, 
                  self.sentiment, keywords_str))
            return cursor.lastrowid