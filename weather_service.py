"""
Weather Service Module
======================
Handles REST API requests to live weather endpoints and parses JSON responses.
Integrates:
1. Open-Meteo Geocoding & Weather REST API (Default: instant, public, no API key required)
2. OpenWeatherMap REST API (Optional: when an API key is provided)
3. Offline fallback dataset for safe offline demonstrations
"""

import json
import os
import requests
from utils import c_to_f, get_weather_description, kmh_to_mph

REQUEST_TIMEOUT = 10


def fetch_open_meteo_weather(city: str) -> dict | None:
    """
    Fetches real-time weather and a 5-day daily forecast using the Open-Meteo REST API.
    Flow:
    1. Geocode city name -> latitude, longitude, country
    2. Query forecast endpoint -> current conditions + daily forecast
    """
    # Step 1: Geocoding
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}

    try:
        geo_resp = requests.get(geo_url, params=geo_params, timeout=REQUEST_TIMEOUT)
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        results = geo_data.get("results")
        if not results:
            print(f"  [!] City '{city}' not found. Please check spelling.")
            return None

        location = results[0]
        lat = location["latitude"]
        lon = location["longitude"]
        city_name = location.get("name", city)
        country = location.get("country", "")

        # Step 2: Forecast query
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,surface_pressure,wind_speed_10m",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "timezone": "auto",
        }

        w_resp = requests.get(weather_url, params=weather_params, timeout=REQUEST_TIMEOUT)
        w_resp.raise_for_status()
        w_data = w_resp.json()

        current = w_data.get("current", {})
        daily = w_data.get("daily", {})

        temp_c = float(current.get("temperature_2m", 0.0))
        feels_c = float(current.get("apparent_temperature", temp_c))
        humidity = int(current.get("relative_humidity_2m", 0))
        wind_kmh = float(current.get("wind_speed_10m", 0.0))
        pressure = int(current.get("surface_pressure", 1013))
        wmo_code = int(current.get("weather_code", 0))

        condition, icon = get_weather_description(wmo_code)

        # Parse 5-day forecast
        forecast_items = []
        dates = daily.get("time", [])[:5]
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        codes = daily.get("weather_code", [])
        precips = daily.get("precipitation_probability_max", [])

        for i in range(len(dates)):
            c_desc, c_icon = get_weather_description(codes[i] if i < len(codes) else 0)
            max_c = max_temps[i] if i < len(max_temps) else temp_c
            min_c = min_temps[i] if i < len(min_temps) else temp_c
            forecast_items.append({
                "date": dates[i],
                "temp_max_c": max_c,
                "temp_max_f": c_to_f(max_c),
                "temp_min_c": min_c,
                "temp_min_f": c_to_f(min_c),
                "condition": c_desc,
                "icon": c_icon,
                "precip_prob": precips[i] if i < len(precips) else 0,
            })

        return {
            "city": city_name,
            "country": country,
            "latitude": lat,
            "longitude": lon,
            "temp_c": temp_c,
            "temp_f": c_to_f(temp_c),
            "feels_like_c": feels_c,
            "feels_like_f": c_to_f(feels_c),
            "humidity": humidity,
            "wind_speed_kmh": wind_kmh,
            "wind_speed_mph": kmh_to_mph(wind_kmh),
            "pressure_hpa": pressure,
            "condition": condition,
            "icon": icon,
            "provider": "Open-Meteo REST API",
            "forecast": forecast_items,
        }

    except requests.exceptions.Timeout:
        print(f"  [Error] Weather API connection timed out.")
        return None
    except requests.exceptions.ConnectionError:
        print(f"  [Error] Network connection failed. Please check internet access.")
        return None
    except Exception as e:
        print(f"  [Error] Failed to parse weather data: {e}")
        return None


def fetch_openweathermap(city: str, api_key: str) -> dict | None:
    """
    Fetches real-time weather from OpenWeatherMap API using a personal API key.
    Endpoint: https://api.openweathermap.org/data/2.5/weather
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        main = data.get("main", {})
        weather_list = data.get("weather", [{}])
        weather_info = weather_list[0] if weather_list else {}
        wind = data.get("wind", {})
        sys_info = data.get("sys", {})

        temp_c = float(main.get("temp", 0.0))
        feels_c = float(main.get("feels_like", temp_c))
        wind_mps = float(wind.get("speed", 0.0))
        wind_kmh = wind_mps * 3.6

        return {
            "city": data.get("name", city),
            "country": sys_info.get("country", ""),
            "latitude": data.get("coord", {}).get("lat", 0.0),
            "longitude": data.get("coord", {}).get("lon", 0.0),
            "temp_c": temp_c,
            "temp_f": c_to_f(temp_c),
            "feels_like_c": feels_c,
            "feels_like_f": c_to_f(feels_c),
            "humidity": int(main.get("humidity", 0)),
            "wind_speed_kmh": wind_kmh,
            "wind_speed_mph": kmh_to_mph(wind_kmh),
            "pressure_hpa": int(main.get("pressure", 1013)),
            "condition": weather_info.get("description", "Clear").title(),
            "icon": "🌤️",
            "provider": "OpenWeatherMap API",
            "forecast": [],
        }
    except requests.exceptions.HTTPError as err:
        if resp.status_code == 401:
            print("  [!] Invalid OpenWeatherMap API key. Falling back to public Open-Meteo API.")
        else:
            print(f"  [Error] OpenWeatherMap request error: {err}")
        return None
    except Exception as e:
        print(f"  [Error] OpenWeatherMap request failed: {e}")
        return None


def get_city_weather(city: str, openweather_key: str | None = None) -> dict | None:
    """
    Unified entry point:
    1. If an OpenWeatherMap API key is provided, attempts OpenWeatherMap.
    2. Otherwise (or on failure), queries the public Open-Meteo REST API.
    """
    if openweather_key:
        result = fetch_openweathermap(city, openweather_key)
        if result:
            return result

    # Default to public Open-Meteo REST API
    return fetch_open_meteo_weather(city)
