import pytest
from app.services.nlp_service import extract_three_most_common_nouns


class TestKeywordExtraction:
    """Test cases for keyword extraction functionality"""

    def test_extract_three_most_common_nouns_basic(self):
        """Test basic noun extraction with simple text"""
        text = "The cat sat on the mat. The dog ran to the park. The cat played with the ball."
        result = extract_three_most_common_nouns(text)
        
        assert len(result) == 3
        assert "cat" in result
        assert result[0] == "cat"

    def test_extract_three_most_common_nouns_complex_text(self):
        """Test noun extraction with more complex text"""
        text = """
        The artificial intelligence system processes natural language data efficiently. 
        Machine learning algorithms analyze text patterns and extract meaningful information 
        from documents. The system uses advanced neural networks and deep learning 
        techniques to understand context and semantics in natural language processing tasks.
        """
        result = extract_three_most_common_nouns(text)
        
        assert len(result) == 3
        assert all(isinstance(noun, str) for noun in result)
        # Should contain technical terms like system, language, learning, etc.
        assert any(noun in ["system", "language", "learning", "networks", "techniques"] for noun in result)

    def test_extract_three_most_common_nouns_repeated_words(self):
        """Test that most frequent nouns are returned first"""
        text = "Python is a programming language. Python developers use Python for data science. Programming requires practice."
        result = extract_three_most_common_nouns(text)
        
        assert len(result) == 3
        assert result[0] == "python"  # most frequent
        # Should contain technical nouns from the text
        expected_nouns = ["python", "language", "developers", "data", "science", "programming", "practice"]
        assert all(noun in expected_nouns for noun in result)

    def test_extract_three_most_common_nouns_fewer_than_three(self):
        """Test text with fewer than 3 unique nouns"""
        text = "The quick brown fox jumps"
        result = extract_three_most_common_nouns(text)
        
        # Should return whatever nouns are found, even if less than 3
        assert len(result) <= 3
        assert "fox" in result

    def test_extract_three_most_common_nouns_no_nouns(self):
        """Test text with no nouns"""
        text = "Run fast!"
        result = extract_three_most_common_nouns(text)
        
        assert len(result) == 0

    def test_extract_three_most_common_nouns_empty_text(self):
        """Test with empty text"""
        text = ""
        result = extract_three_most_common_nouns(text)
        
        assert len(result) == 0

    def test_extract_three_most_common_nouns_mixed_case(self):
        """Test that function handles mixed case properly"""
        text = "The Database stores data. DATABASE management requires skills. Data analysis is important."
        result = extract_three_most_common_nouns(text)
        
        assert len(result) >= 2
        # All results should be lowercase
        assert all(noun.islower() for noun in result)
        assert "database" in result or "data" in result

    def test_extract_three_most_common_nouns_technical_content(self):
        """Test with technical content similar to real use case"""
        text = """
        Cloud computing infrastructure requires robust security measures. 
        The server architecture handles multiple requests simultaneously. 
        Database optimization improves application performance significantly. 
        Security protocols protect user data and system integrity.
        """
        result = extract_three_most_common_nouns(text)
        
        assert len(result) == 3
        # Should extract technical nouns
        expected_nouns = ["security", "system", "data", "server", "application", "database"]
        assert any(noun in expected_nouns for noun in result)