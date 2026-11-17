"""
Utility functions, unit conversions, and weather code mappers.
Internship Project 05: Weather App with Live OpenWeather API.
"""

import sys

# Standard WMO Weather Interpretation Codes to human readable descriptions & emojis
WMO_WEATHER_CODES = {
    0: ("Clear Sky", "☀️"),
    1: ("Mainly Clear", "🌤️"),
    2: ("Partly Cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Rime Fog", "🌫️"),
    51: ("Light Drizzle", "🌦️"),
    53: ("Moderate Drizzle", "🌦️"),
    55: ("Dense Drizzle", "🌧️"),
    61: ("Slight Rain", "🌦️"),
    63: ("Moderate Rain", "🌧️"),
    65: ("Heavy Rain", "🌧️"),
    71: ("Slight Snow", "🌨️"),
    73: ("Moderate Snow", "❄️"),
    75: ("Heavy Snow", "❄️"),
    80: ("Rain Showers", "🌦️"),
    81: ("Moderate Showers", "🌧️"),
    82: ("Violent Showers", "⛈️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with Hail", "⛈️"),
    99: ("Severe Thunderstorm with Hail", "⛈️"),
}


def get_weather_description(code: int) -> tuple[str, str]:
    """Returns (description, emoji_icon) for a given WMO code."""
    return WMO_WEATHER_CODES.get(code, ("Variable Conditions", "🌡️"))


def c_to_f(celsius: float) -> float:
    """Converts Celsius to Fahrenheit."""
    return (celsius * 9.0 / 5.0) + 32.0


def kmh_to_mph(kmh: float) -> float:
    """Converts km/h to mph."""
    return kmh * 0.621371


def show_header(title: str, line_char: str = "=") -> None:
    """Prints a styled header line for terminal menus."""
    width = 64
    bar = line_char * width
    print(f"\n{bar}")
    print(f" {title.upper()}")
    print(f"{bar}")


def show_divider(length: int = 64) -> None:
    """Prints a simple horizontal separator."""
    print("-" * length)


def read_choice(prompt: str, valid_options: list[str]) -> str:
    """Prompts for and validates menu choices (case-insensitive)."""
    opts = [opt.strip().upper() for opt in valid_options]
    while True:
        try:
            user_input = input(prompt).strip().upper()
            if user_input in opts:
                return user_input
            print(f"   [!] Please pick one of: {', '.join(opts)}")
        except (KeyboardInterrupt, EOFError):
            print("\n   [!] Exiting.")
            sys.exit(0)


def pause() -> None:
    """Pauses until user presses Enter."""
    try:
        input("\nPress Enter to continue...")
    except (KeyboardInterrupt, EOFError):
        sys.exit(0)
