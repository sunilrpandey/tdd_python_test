"""
Weather service client to demonstrate mocking.
"""
import requests
from typing import Dict, Optional

class WeatherService:
    """A client for getting weather information."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.weather.com"):
        """Initialize the weather service client."""
        self.api_key = api_key
        self.base_url = base_url
    
    def get_current_temperature(self, city: str) -> Optional[float]:
        """Get the current temperature for a city."""
        try:
            response = requests.get(
                f"{self.base_url}/current",
                params={"city": city, "api_key": self.api_key},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            return data["temperature"]
        except (requests.RequestException, KeyError):
            return None
    
    def get_forecast(self, city: str, days: int = 5) -> Optional[Dict]:
        """Get the weather forecast for a city."""
        try:
            response = requests.get(
                f"{self.base_url}/forecast",
                params={
                    "city": city,
                    "days": days,
                    "api_key": self.api_key
                },
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None
    
    def update_api_key(self, new_key: str) -> bool:
        """Update the API key."""
        try:
            response = requests.post(
                f"{self.base_url}/validate",
                json={"api_key": new_key},
                timeout=5
            )
            response.raise_for_status()
            if response.json()["valid"]:
                self.api_key = new_key
                return True
            return False
        except requests.RequestException:
            return False