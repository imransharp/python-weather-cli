import os
import requests
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str) -> dict:
    """Fetch weather data for a given city from OpenWeather API."""
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

def show_weather(data: dict):
    """Print formatted weather information."""
    if data.get("cod") != 200:
        print("❌ City not found. Please check spelling.")
        return

    city = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    desc = data["weather"][0]["description"].capitalize()

    print(f"\n🌍 Weather in {city}, {country}:")
    print(f"🌡 Temperature: {temp}°C")
    print(f"💧 Humidity: {humidity}%")
    print(f"☁️ Condition: {desc}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python weather.py <city>")
        sys.exit(1)

    city = " ".join(sys.argv[1:])
    data = get_weather(city)
    show_weather(data)
