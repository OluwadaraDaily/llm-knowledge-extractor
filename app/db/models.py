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
    
    @classmethod
    async def search_by_keyword(cls, keyword: str) -> List['Analysis']:
        """Search analyses by keyword in keywords field."""
        async with get_db_connection() as conn:
            cursor = await conn.execute("""
                SELECT * FROM analyses 
                WHERE keywords LIKE ?
                ORDER BY created_at DESC
            """, (f'%"{keyword}"%',))
            rows = await cursor.fetchall()
            return [cls._from_row(row) for row in rows]
    
    @classmethod
    async def search_by_sentiment(cls, sentiment: str) -> List['Analysis']:
        """Search analyses by sentiment."""
        async with get_db_connection() as conn:
            cursor = await conn.execute("""
                SELECT * FROM analyses 
                WHERE sentiment = ?
                ORDER BY created_at DESC
            """, (sentiment,))
            rows = await cursor.fetchall()
            return [cls._from_row(row) for row in rows]
    
    @classmethod
    def _from_row(cls, row) -> 'Analysis':
        """Create Analysis instance from database row."""
        topics = json.loads(row['topics']) if row['topics'] else []
        keywords = json.loads(row['keywords']) if row['keywords'] else []
        
        analysis = cls(
            input_text=row['input_text'],
            summary=row['summary'] or "",
            title=row['title'] or "",
            topics=topics,
            sentiment=row['sentiment'] or "",
            keywords=keywords
        )
        analysis.id = row['id']
        analysis.created_at = row['created_at']
        return analysis