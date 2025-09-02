from .fixtures import client


class TestSearchEndpoints:
    """Simple integration tests for search endpoints."""
    
    def test_search_endpoint_no_parameters(self, client):
        """Test search endpoint returns error without parameters."""
        response = client.get("/search")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert data["error"] == "No keyword or sentiment provided"
    
    def test_search_endpoint_with_keyword(self, client):
        """Test search endpoint with keyword parameter."""
        response = client.get("/search?keyword=python")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
    
    def test_search_endpoint_with_sentiment(self, client):
        """Test search endpoint with sentiment parameter."""
        response = client.get("/search?sentiment=positive")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
    
    def test_search_endpoint_response_structure(self, client):
        """Test search response includes expected fields when results exist."""
        response = client.get("/search?keyword=test")
        assert response.status_code == 200
        data = response.json()
        
        # If there are results, check structure
        if data["data"]:
            result = data["data"][0]
            expected_fields = {"id", "input_text", "summary", "title", "topics", 
                             "sentiment", "keywords", "created_at"}
            assert all(field in result for field in expected_fields)