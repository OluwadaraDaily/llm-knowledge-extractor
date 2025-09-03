import pytest
import json
from unittest.mock import Mock, patch
from app.services.openai_service import analyze_text
from app.db.models import Analysis


class TestJSONSchemaValidation:
    """Test cases for JSON schema validation"""

    def test_openai_response_schema_valid(self):
        """Test that OpenAI service returns expected schema format"""
        expected_keys = {"summary", "title", "key_topics", "sentiment"}
        
        mock_response = {
            "summary": "This is a test summary",
            "title": "Test Title", 
            "key_topics": ["topic1", "topic2", "topic3"],
            "sentiment": "positive"
        }
        
        with patch('app.services.openai_service.client') as mock_client:
            mock_completion = Mock()
            mock_choice = Mock()
            mock_message = Mock()
            mock_message.content = json.dumps(mock_response)
            mock_choice.message = mock_message
            mock_completion.choices = [mock_choice]
            mock_client.chat.completions.create.return_value = mock_completion
            
            result = analyze_text("test text")
            
            assert all(key in result for key in expected_keys)
            assert isinstance(result["summary"], str)
            assert isinstance(result["title"], str) or result["title"] is None
            assert isinstance(result["key_topics"], list)
            assert result["sentiment"] in ["positive", "negative", "neutral"]

    def test_openai_response_schema_with_null_title(self):
        """Test schema validation when title is null"""
        mock_response = {
            "summary": "This is a test summary",
            "title": None,
            "key_topics": ["topic1", "topic2"],
            "sentiment": "neutral"
        }
        
        with patch('app.services.openai_service.client') as mock_client:
            mock_completion = Mock()
            mock_choice = Mock()
            mock_message = Mock()
            mock_message.content = json.dumps(mock_response)
            mock_choice.message = mock_message
            mock_completion.choices = [mock_choice]
            mock_client.chat.completions.create.return_value = mock_completion
            
            result = analyze_text("test text")
            
            assert result["title"] is None
            assert isinstance(result["summary"], str)
            assert isinstance(result["key_topics"], list)
            assert result["sentiment"] in ["positive", "negative", "neutral"]

    def test_openai_response_schema_invalid_json(self):
        """Test error handling for invalid JSON response"""
        with patch('app.services.openai_service.client') as mock_client:
            mock_completion = Mock()
            mock_choice = Mock()
            mock_message = Mock()
            mock_message.content = "Invalid JSON response"
            mock_choice.message = mock_message
            mock_completion.choices = [mock_choice]
            mock_client.chat.completions.create.return_value = mock_completion
            
            result = analyze_text("test text")
            
            assert "error" in result
            assert result["error"] == "Failed to parse JSON response"
            assert "raw_response" in result

    def test_analysis_model_schema_validation(self):
        """Test that Analysis model creates proper structure"""
        # Create Analysis instance
        analysis = Analysis(
            input_text="Sample text for analysis",
            summary="This is a summary",
            title="Sample Title",
            topics=["technology", "AI", "machine learning"],
            sentiment="positive",
            keywords=["python", "data", "analysis"]
        )
        
        # Verify all required fields are present
        assert analysis.input_text == "Sample text for analysis"
        assert analysis.summary == "This is a summary"
        assert analysis.title == "Sample Title"
        assert isinstance(analysis.topics, list)
        assert len(analysis.topics) == 3
        assert analysis.sentiment == "positive"
        assert isinstance(analysis.keywords, list)
        assert len(analysis.keywords) == 3

    def test_analysis_model_with_defaults(self):
        """Test Analysis model with default values"""
        analysis = Analysis(input_text="Test text")
        
        assert analysis.input_text == "Test text"
        assert analysis.summary == ""
        assert analysis.title == ""
        assert analysis.topics == []
        assert analysis.sentiment == ""
        assert analysis.keywords == []

    def test_complete_response_schema(self):
        """Test the complete response schema from the /analyze endpoint"""
        # Mock both services
        openai_response = {
            "summary": "Test analysis summary",
            "title": "Test Document",
            "key_topics": ["AI", "machine learning", "data science"],
            "sentiment": "positive"
        }
        
        nlp_response = ["data", "science", "analysis"]
        
        with patch('app.services.openai_service.client') as mock_client:
            mock_completion = Mock()
            mock_choice = Mock()
            mock_message = Mock()
            mock_message.content = json.dumps(openai_response)
            mock_choice.message = mock_message
            mock_completion.choices = [mock_choice]
            mock_client.chat.completions.create.return_value = mock_completion
            
            with patch('app.services.nlp_service.extract_three_most_common_nouns') as mock_nlp:
                mock_nlp.return_value = nlp_response
                
                # Simulate the endpoint logic
                openai_result = analyze_text("test text")
                nlp_result = nlp_response
                
                complete_response = {
                    **openai_result,
                    "keywords": nlp_result
                }
                
                # Verify complete schema
                expected_keys = {"summary", "title", "key_topics", "sentiment", "keywords"}
                assert all(key in complete_response for key in expected_keys)
                
                # Verify data types
                assert isinstance(complete_response["summary"], str)
                assert isinstance(complete_response["title"], str) or complete_response["title"] is None
                assert isinstance(complete_response["key_topics"], list)
                assert complete_response["sentiment"] in ["positive", "negative", "neutral"]
                assert isinstance(complete_response["keywords"], list)
                assert len(complete_response["keywords"]) <= 3