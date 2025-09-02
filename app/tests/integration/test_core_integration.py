import json
from unittest.mock import patch, Mock
from .fixtures import client


class TestCoreIntegration:
    """Simple core integration tests."""
    
    def test_root_endpoint(self, client):
        """Test the root endpoint returns Hello World."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}
    
    def test_analyze_endpoint_success(self, client):
        """Test POST /analyze returns valid response with all fields."""
        mock_openai_response = {
            "summary": "Test summary",
            "title": "Test Title",
            "key_topics": ["test", "integration"],
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
            
            response = client.post("/analyze", json={"text": "Test text for analysis"})
            
            assert response.status_code == 200
            data = response.json()
            
            # Check required fields
            assert "summary" in data
            assert "title" in data
            assert "key_topics" in data
            assert "sentiment" in data
            assert "keywords" in data
    
    def test_analyze_endpoint_invalid_input(self, client):
        """Test analyze endpoint with invalid input returns 422."""
        response = client.post("/analyze", json={"wrong_field": "test"})
        assert response.status_code == 422
    
    def test_search_endpoint_no_parameters(self, client):
        """Test search endpoint returns error without parameters."""
        response = client.get("/search")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data