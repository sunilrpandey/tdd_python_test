"""
Tests for WeatherService class demonstrating mocking.
"""
import pytest
from unittest.mock import Mock, patch
from weather_service import WeatherService

# Test data
MOCK_API_KEY = "test_api_key"
MOCK_BASE_URL = "https://test.weather.com"
MOCK_CITY = "London"

@pytest.fixture
def weather_service():
    """Create a WeatherService instance."""
    return WeatherService(MOCK_API_KEY, MOCK_BASE_URL)

def test_get_current_temperature(weather_service, mocker):
    """Test getting current temperature with mocked requests."""
    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = {"temperature": 25.5}
    
    # Mock requests.get
    mock_get = mocker.patch('requests.get', return_value=mock_response)
    
    # Get temperature
    temp = weather_service.get_current_temperature(MOCK_CITY)
    
    # Assertions
    assert temp == 25.5
    mock_get.assert_called_once_with(
        f"{MOCK_BASE_URL}/current",
        params={"city": MOCK_CITY, "api_key": MOCK_API_KEY},
        timeout=5
    )

def test_get_current_temperature_error(weather_service, mocker):
    """Test handling of API errors."""
    # Mock requests.get to raise an exception
    mocker.patch('requests.get', side_effect=Exception("API Error"))
    
    # Get temperature
    temp = weather_service.get_current_temperature(MOCK_CITY)
    
    # Should return None on error
    assert temp is None

def test_get_forecast(weather_service, mocker):
    """Test getting forecast with mocked requests."""
    # Mock forecast data
    mock_forecast = {
        "daily": [
            {"temp": 20, "condition": "Sunny"},
            {"temp": 22, "condition": "Cloudy"}
        ]
    }
    
    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = mock_forecast
    
    # Mock requests.get
    mock_get = mocker.patch('requests.get', return_value=mock_response)
    
    # Get forecast
    forecast = weather_service.get_forecast(MOCK_CITY, days=2)
    
    # Assertions
    assert forecast == mock_forecast
    mock_get.assert_called_once_with(
        f"{MOCK_BASE_URL}/forecast",
        params={"city": MOCK_CITY, "days": 2, "api_key": MOCK_API_KEY},
        timeout=5
    )

@pytest.mark.parametrize("api_response,expected", [
    ({"valid": True}, True),
    ({"valid": False}, False)
])
def test_update_api_key(weather_service, mocker, api_response, expected):
    """Test API key updates with parameterized responses."""
    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = api_response
    
    # Mock requests.post
    mock_post = mocker.patch('requests.post', return_value=mock_response)
    
    # Update API key
    new_key = "new_test_key"
    result = weather_service.update_api_key(new_key)
    
    # Assertions
    assert result == expected
    if expected:
        assert weather_service.api_key == new_key
    else:
        assert weather_service.api_key == MOCK_API_KEY
    
    mock_post.assert_called_once_with(
        f"{MOCK_BASE_URL}/validate",
        json={"api_key": new_key},
        timeout=5
    )