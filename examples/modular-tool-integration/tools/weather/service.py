"""Service helper for weather data.

This module provides mock weather data for the travel assistant example.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""


def get_mock_weather(city: str) -> str:
    """Simulates a complex service call in a helper file.

    Args:
        city: The name of the city to get weather for.

    Returns:
        A string containing the mock weather forecast.
    """
    return f"The weather in {city} is sunny, 25°C."
