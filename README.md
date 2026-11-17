# Python Internship Project 05 (Capstone): Weather App with Live OpenWeather API

**Submitted by:** Yashraj  
**Technology:** Python 3.10+, Requests, Tkinter, REST APIs  
**Project Category:** Capstone Project — Real-World Cloud REST API Integration & Data Parsing  

---

## 1. Project Overview

This repository represents the **Capstone Project (Project 05)** of my Python Developer Internship: an end-to-end **Live Weather Application** that interfaces with real-time cloud meteorological APIs to fetch, parse, and present current atmospheric conditions and multi-day forecasts for any city worldwide.

The project demonstrates:
- Connecting Python applications to production REST APIs using `requests`.
- Multi-step API workflows: geocoding city names into geographical coordinates, followed by live forecast queries.
- Parsing and structuring complex JSON payloads (temperatures, apparent feels-like, humidity, wind speeds, atmospheric pressure, and WMO weather codes).
- Dual user interface design: a structured terminal CLI (`main.py`) and a desktop graphical user interface using Python's built-in `tkinter` module (`gui.py`).
- Hybrid API engine: supports custom OpenWeatherMap API keys while offering keyless, real-time public REST API integration (via Open-Meteo) so the application works out-of-the-box without registration delays.
- A client-side web showcase (`index.html`) deployed to GitHub Pages for instant interactive testing in any browser.

---

## 2. Project Architecture

The project is structured into modular layers separating network communication, data transformations, graphical displays, and CLI flows:

```text
weather_app_live_api/
│
├── main.py              # Interactive CLI menu loop and formatted terminal displays
├── gui.py               # Desktop GUI application built with Python's built-in tkinter
├── weather_service.py   # REST API client handling requests and JSON response parsing
├── utils.py             # Temperature conversions (°C/°F), wind conversions, and WMO codes
├── sample_weather.json  # Reference JSON payload and offline fallback dataset
├── requirements.txt     # Dependencies (requests>=2.31.0)
├── test_app.py          # Automated unit test suite (conversions, code mappings, JSON parsing)
├── index.html           # Standalone web demo for GitHub Pages
├── .gitignore           # Excludes local caches and runtime reports
└── README.md            # Capstone project report and guide
```

---

## 3. Technical Implementation & Data Flow

### 1. Two-Stage REST API Request Pipeline
When a user enters a city name (e.g. *Mumbai*, *London*, *New York*):
1. **Geocoding Stage:** The application queries the geocoding endpoint to convert the user's string into high-precision latitude, longitude, and country metadata.
2. **Forecast Stage:** The coordinates are passed into the weather endpoint, requesting `temperature_2m`, `apparent_temperature`, `relative_humidity_2m`, `surface_pressure`, `wind_speed_10m`, and daily min/max bounds.

### 2. JSON Response Parsing & WMO Code Mapping
The raw JSON response contains standard meteorological WMO weather interpretation codes. In `utils.py`, `get_weather_description()` maps integer codes (such as code 0 for *Clear Sky ☀️*, code 61 for *Slight Rain 🌦️*, code 95 for *Thunderstorm ⛈️*) to clean human-readable descriptions and visual weather icons.

### 3. Dual UI Displays
- **Terminal CLI (`main.py`):** Renders formatted ASCII cards displaying current parameters, coordinates, data sources, and an aligned 5-day daily forecast table with precipitation probabilities.
- **Desktop Tkinter GUI (`gui.py`):** A modern desktop window featuring real-time city search, a big temperature display, an instant °C / °F toggle button, parameter metric tiles, and horizontal 5-day forecast cards.

---

## 4. How to Run the Application

### 1. Installation
Clone the repository and install the requirements:

```bash
cd weather_app_live_api
pip install -r requirements.txt
```

### 2. Running the Terminal CLI Application
Launch the terminal interface:

```bash
python main.py
```

### 3. Running the Desktop Tkinter GUI
Launch the desktop graphical application:

```bash
python gui.py
```
*(You can also launch the GUI directly from Option 5 in the CLI menu).*

### 4. Running the Automated Tests
Run the unit test suite:

```bash
python -m unittest test_app.py
```

Expected output:
```text
....
----------------------------------------------------------------------
Ran 4 tests in 0.009s

OK
```

---

## 5. Sample CLI Run

```text
================================================================
 WEATHER FOR: Mumbai, India
================================================================
  Condition:       🌤️  Mainly Clear
  Temperature:     31.4°C (Feels like 33.8°C)
  Humidity:        61%
  Wind Speed:      11.8 km/h
  Pressure:        1011 hPa
  Coordinates:     19.07° N, 72.88° E
  Data Source:     Open-Meteo REST API
----------------------------------------------------------------
  5-DAY EXTENDED FORECAST:
  Date         | High     | Low      | Rain %   | Condition
  --------------------------------------------------------
  2026-11-17   | 33°C     | 24°C     | 0%       | ☀️ Clear Sky
  2026-11-18   | 32°C     | 23°C     | 0%       | 🌤️ Mainly Clear
  2026-11-19   | 32°C     | 23°C     | 0%       | 🌤️ Mainly Clear
  2026-11-20   | 31°C     | 22°C     | 0%       | ☀️ Clear Sky
  2026-11-21   | 31°C     | 22°C     | 0%       | ☀️ Clear Sky
================================================================
```
