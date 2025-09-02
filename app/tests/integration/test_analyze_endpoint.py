import json
from unittest.mock import patch, Mock
from .fixtures import client


class TestAnalyzeEndpoint:
    """Simple integration tests for POST /analyze endpoint."""
    
    def test_analyze_endpoint_success(self, client):
        """Test successful analysis returns all required fields."""
        mock_openai_response = {
            "summary": "Test summary about technology",
            "title": "Technology Overview",
            "key_topics": ["technology", "testing"],
            "sentiment": "positive"
        }
        
        with patch('app.services.openai_service.client') as mock_client:
            mock_completion = Mock()
            mock_choice = Mock()
            mock_message = Mock()
            mock_message.content = json.dumps(mock_openai_response)
            mock_choice.message = mock_message
            mock_completion.choices = [mock_choice]
            mock_client.chat.completions.create.return_value = mock_completion
            
            response = client.post("/analyze", json={"text": "Technology is advancing rapidly."})
            
            assert response.status_code == 200
            data = response.json()
            
            # Check all required fields present
            assert "summary" in data
            assert "title" in data
            assert "key_topics" in data
            assert "sentiment" in data
            assert "keywords" in data
    
    def test_analyze_endpoint_with_null_title(self, client):
        """Test analysis handles null title correctly."""
        mock_openai_response = {
            "summary": "Test summary",
            "title": None,
            "key_topics": ["testing"],
            "sentiment": "neutral"
        }
        
        with patch('app.services.openai_service.client') as mock_client:
            mock_completion = Mock()
            mock_choice = Mock()
            mock_message = Mock()
            mock_message.content = json.dumps(mock_openai_response)
            mock_choice.message = mock_message
            mock_completion.choices = [mock_choice]
            mock_client.chat.completions.create.return_value = mock_completion
            
            response = client.post("/analyze", json={"text": "Test text."})
            
            assert response.status_code == 200
            data = response.json()
            assert data["title"] is None
    
    def test_analyze_endpoint_invalid_input(self, client):
        """Test endpoint returns 422 for invalid input."""
        response = client.post("/analyze", json={"wrong_field": "text"})
        assert response.status_code == 422
    
    def test_analyze_endpoint_error_handling(self, client):
        """Test endpoint handles OpenAI errors gracefully."""
        with patch('app.services.openai_service.client') as mock_client:
            mock_completion = Mock()
            mock_choice = Mock()
            mock_message = Mock()
            mock_message.content = "Invalid JSON response"
            mock_choice.message = mock_message
            mock_completion.choices = [mock_choice]
            mock_client.chat.completions.create.return_value = mock_completion
            
            response = client.post("/analyze", json={"text": "Test text"})
            
            assert response.status_code == 200
            data = response.json()
            assert "error" in data