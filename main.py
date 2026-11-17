"""
CLI Application: Weather App with Live OpenWeather & Open-Meteo API
Internship Project 05 - Python 3.10+ (Capstone Project)
"""

import json
import os
import subprocess
import sys
from utils import pause, read_choice, show_divider, show_header
from weather_service import get_city_weather

# Application state
config = {
    "unit": "C",  # "C" or "F"
    "openweather_api_key": os.getenv("OPENWEATHER_API_KEY", ""),
    "last_result": None,
}


def print_weather_card(data: dict, unit: str = "C") -> None:
    """Renders a beautifully structured terminal card for live weather & forecast."""
    city = data["city"]
    country = data.get("country", "")
    full_loc = f"{city}, {country}" if country else city

    temp_str = f"{data['temp_c']:.1f}°C" if unit == "C" else f"{data['temp_f']:.1f}°F"
    feels_str = f"{data['feels_like_c']:.1f}°C" if unit == "C" else f"{data['feels_like_f']:.1f}°F"
    wind_str = f"{data['wind_speed_kmh']:.1f} km/h" if unit == "C" else f"{data['wind_speed_mph']:.1f} mph"

    show_header(f"WEATHER FOR: {full_loc}")
    print(f"  Condition:       {data['icon']}  {data['condition']}")
    print(f"  Temperature:     {temp_str} (Feels like {feels_str})")
    print(f"  Humidity:        {data['humidity']}%")
    print(f"  Wind Speed:      {wind_str}")
    print(f"  Pressure:        {data['pressure_hpa']} hPa")
    print(f"  Coordinates:     {data['latitude']:.2f}° N, {data['longitude']:.2f}° E")
    print(f"  Data Source:     {data.get('provider', 'REST API')}")
    show_divider()

    # 5-day Forecast table
    forecast = data.get("forecast", [])
    if forecast:
        print("  5-DAY EXTENDED FORECAST:")
        print(f"  {'Date':<12} | {'High':<8} | {'Low':<8} | {'Rain %':<8} | {'Condition'}")
        print("  " + "-" * 56)
        for day in forecast:
            high = f"{day['temp_max_c']:.0f}°C" if unit == "C" else f"{day['temp_max_f']:.0f}°F"
            low = f"{day['temp_min_c']:.0f}°C" if unit == "C" else f"{day['temp_min_f']:.0f}°F"
            rain = f"{day.get('precip_prob', 0)}%"
            cond = f"{day.get('icon', '')} {day.get('condition', '')}"
            print(f"  {day['date']:<12} | {high:<8} | {low:<8} | {rain:<8} | {cond}")
        show_divider()


def export_weather_dialog(data: dict) -> None:
    """Exports weather data to a local file."""
    if not data:
        print("  [!] No weather data available to export.")
        return

    print("\n  Export Options:")
    print("  1. Save JSON Report (.json)")
    print("  2. Save Text Summary (.txt)")
    print("  3. Cancel")
    show_divider()

    choice = read_choice("  Select option (1-3): ", ["1", "2", "3"])
    city_slug = data["city"].lower().replace(" ", "_")

    if choice == "1":
        filename = f"weather_{city_slug}.json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"  ✅ Saved JSON report to '{filename}'")
        except Exception as e:
            print(f"  [Error] Failed to write JSON: {e}")

    elif choice == "2":
        filename = f"weather_{city_slug}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"WEATHER REPORT: {data['city']}, {data.get('country', '')}\n")
                f.write(f"Condition:   {data['condition']}\n")
                f.write(f"Temperature: {data['temp_c']} C ({data['temp_f']:.1f} F)\n")
                f.write(f"Feels Like:  {data['feels_like_c']} C\n")
                f.write(f"Humidity:    {data['humidity']}%\n")
                f.write(f"Wind Speed:  {data['wind_speed_kmh']} km/h\n")
                f.write(f"Pressure:    {data['pressure_hpa']} hPa\n")
            print(f"  ✅ Saved text summary to '{filename}'")
        except Exception as e:
            print(f"  [Error] Failed to write TXT: {e}")


def launch_tkinter_gui() -> None:
    """Launches the Tkinter GUI in a non-blocking process."""
    try:
        gui_path = os.path.join(os.path.dirname(__file__), "gui.py")
        subprocess.Popen([sys.executable, gui_path])
        print("  🚀 Desktop GUI launched in a new window!")
    except Exception as e:
        print(f"  [Error] Could not launch GUI: {e}")


def main() -> None:
    """Main application loop."""
    show_header("Weather App with Live OpenWeather API")
    print(" Project 05: Capstone REST API Integration & Data Parsing")
    print(" Powered by Open-Meteo & OpenWeatherMap REST APIs")
    show_divider()

    while True:
        unit_label = "Celsius (°C)" if config["unit"] == "C" else "Fahrenheit (°F)"
        show_header(f"Weather Main Menu [Active Unit: {unit_label}]")
        print("  1. Search Live City Weather & 5-Day Forecast")
        print("  2. Quick View Global Hubs (Mumbai, London, New York, Tokyo)")
        print("  3. Toggle Temperature Unit (°C / °F)")
        print("  4. Set OpenWeatherMap API Key (Optional)")
        print("  5. Launch Desktop GUI (Tkinter Window)")
        print("  6. Export Current Weather Report (JSON / TXT)")
        print("  7. Exit Application")
        show_divider()

        choice = read_choice("  Enter your selection (1-7): ", ["1", "2", "3", "4", "5", "6", "7"])

        if choice == "1":
            city_name = input("\n  Enter city name (e.g. Pune, London, Sydney): ").strip()
            if not city_name:
                print("  [!] City name cannot be blank.")
                pause()
                continue

            print(f"  Connecting to live REST weather API for '{city_name}'...")
            data = get_city_weather(city_name, config["openweather_api_key"])
            if data:
                config["last_result"] = data
                print_weather_card(data, config["unit"])
            else:
                print(f"  [!] Unable to fetch weather for '{city_name}'.")
            pause()

        elif choice == "2":
            show_header("Global Cities Quick View")
            hubs = ["Mumbai", "London", "New York", "Tokyo", "Paris"]
            for hub in hubs:
                data = get_city_weather(hub, config["openweather_api_key"])
                if data:
                    t = f"{data['temp_c']:.1f}°C" if config["unit"] == "C" else f"{data['temp_f']:.1f}°F"
                    print(f"  • {data['city']:<10} | {data['icon']} {data['condition']:<16} | Temp: {t:<8} | Humidity: {data['humidity']}%")
            show_divider()
            pause()

        elif choice == "3":
            config["unit"] = "F" if config["unit"] == "C" else "C"
            new_label = "Celsius (°C)" if config["unit"] == "C" else "Fahrenheit (°F)"
            print(f"\n  ✅ Temperature unit changed to {new_label}.")
            pause()

        elif choice == "4":
            show_header("OpenWeatherMap API Key Configuration")
            print("  Note: An API key is optional! The app uses public Open-Meteo REST API by default.")
            current_key = config["openweather_api_key"] or "None (Using Public API)"
            print(f"  Current API Key: {current_key}")
            new_key = input("  Enter your OpenWeatherMap API key (or press Enter to keep current): ").strip()
            if new_key:
                config["openweather_api_key"] = new_key
                print("  ✅ OpenWeatherMap API key updated.")
            pause()

        elif choice == "5":
            launch_tkinter_gui()
            pause()

        elif choice == "6":
            if config["last_result"]:
                export_weather_dialog(config["last_result"])
            else:
                print("\n  [!] Please search for a city first before exporting.")
            pause()

        elif choice == "7":
            print("\n  Thank you for using the Live Weather App. Have a sunny day! ☀️\n")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n  Session closed by user. Exiting cleanly.")
        sys.exit(0)
