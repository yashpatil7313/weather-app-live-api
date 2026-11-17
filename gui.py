"""
Desktop GUI Interface for Weather App
=====================================
Built using Python's standard library `tkinter` module.
Features:
- Live city search
- Temperature unit toggle (°C / °F)
- Detailed metrics card (Feels Like, Humidity, Wind, Pressure)
- 5-day horizontal forecast cards
"""

import sys
import tkinter as tk
from tkinter import messagebox, ttk
from utils import c_to_f, kmh_to_mph
from weather_service import get_city_weather


class WeatherAppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App - Live OpenWeather API")
        self.geometry("640x660")
        self.minsize(580, 600)
        self.configure(bg="#f8fafc")

        self.current_unit = "C"
        self.current_data = None

        self._build_ui()
        # Pre-load a default city
        self.search_city("Mumbai")

    def _build_ui(self):
        # Header title
        header_frame = tk.Frame(self, bg="#2563eb", pady=14)
        header_frame.pack(fill=tk.X)

        title_lbl = tk.Label(header_frame, text="🌤️ Live Weather Application", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#2563eb")
        title_lbl.pack()
        sub_lbl = tk.Label(header_frame, text="Capstone Project: REST API Integration & JSON Parsing", font=("Segoe UI", 9), fg="#bfdbfe", bg="#2563eb")
        sub_lbl.pack()

        # Search bar
        search_frame = tk.Frame(self, bg="#f8fafc", pady=12)
        search_frame.pack(fill=tk.X, padx=20)

        self.city_entry = tk.Entry(search_frame, font=("Segoe UI", 12), width=28, relief=tk.SOLID, bd=1)
        self.city_entry.pack(side=tk.LEFT, ipady=4, expand=True, fill=tk.X)
        self.city_entry.insert(0, "Mumbai")
        self.city_entry.bind("<Return>", lambda e: self.on_search())

        search_btn = tk.Button(search_frame, text="Search City", font=("Segoe UI", 10, "bold"), bg="#2563eb", fg="#ffffff", padx=12, relief=tk.FLAT, command=self.on_search, cursor="hand2")
        search_btn.pack(side=tk.LEFT, padx=(8, 0))

        self.unit_btn = tk.Button(search_frame, text="°C", font=("Segoe UI", 10, "bold"), bg="#e2e8f0", fg="#1e293b", padx=10, relief=tk.FLAT, command=self.toggle_unit, cursor="hand2")
        self.unit_btn.pack(side=tk.LEFT, padx=(8, 0))

        # Main Weather Display Card
        self.card = tk.Frame(self, bg="#ffffff", bd=1, relief=tk.SOLID, padx=20, pady=18)
        self.card.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        self.loc_label = tk.Label(self.card, text="Loading City...", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#0f172a")
        self.loc_label.pack(anchor="w")

        self.condition_label = tk.Label(self.card, text="--", font=("Segoe UI", 12), bg="#ffffff", fg="#64748b")
        self.condition_label.pack(anchor="w", pady=(2, 10))

        # Big Temp display
        self.temp_label = tk.Label(self.card, text="--°", font=("Segoe UI", 36, "bold"), bg="#ffffff", fg="#1e293b")
        self.temp_label.pack(anchor="w")

        self.feels_label = tk.Label(self.card, text="Feels like: --", font=("Segoe UI", 10), bg="#ffffff", fg="#64748b")
        self.feels_label.pack(anchor="w", pady=(0, 14))

        # Metrics grid (Humidity, Wind, Pressure, Lat/Lon)
        metrics_frame = tk.Frame(self.card, bg="#f1f5f9", padx=12, pady=10)
        metrics_frame.pack(fill=tk.X, pady=(0, 14))

        self.hum_lbl = tk.Label(metrics_frame, text="💧 Humidity: --", font=("Segoe UI", 10), bg="#f1f5f9", fg="#334155")
        self.hum_lbl.grid(row=0, column=0, sticky="w", padx=10, pady=4)

        self.wind_lbl = tk.Label(metrics_frame, text="💨 Wind: --", font=("Segoe UI", 10), bg="#f1f5f9", fg="#334155")
        self.wind_lbl.grid(row=0, column=1, sticky="w", padx=10, pady=4)

        self.press_lbl = tk.Label(metrics_frame, text="⏲️ Pressure: --", font=("Segoe UI", 10), bg="#f1f5f9", fg="#334155")
        self.press_lbl.grid(row=1, column=0, sticky="w", padx=10, pady=4)

        self.coords_lbl = tk.Label(metrics_frame, text="📍 Coords: --", font=("Segoe UI", 10), bg="#f1f5f9", fg="#334155")
        self.coords_lbl.grid(row=1, column=1, sticky="w", padx=10, pady=4)

        # 5-day Forecast Label
        tk.Label(self.card, text="5-Day Daily Forecast:", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#1e293b").pack(anchor="w", pady=(0, 6))

        # Forecast items frame
        self.forecast_frame = tk.Frame(self.card, bg="#ffffff")
        self.forecast_frame.pack(fill=tk.X)

        # Status footer
        self.status_lbl = tk.Label(self, text="Ready", font=("Segoe UI", 8), bg="#f8fafc", fg="#94a3b8")
        self.status_lbl.pack(side=tk.BOTTOM, fill=tk.X, pady=4)

    def on_search(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please type a city name.")
            return
        self.search_city(city)

    def search_city(self, city: str):
        self.status_lbl.config(text=f"Connecting to REST API for '{city}'...")
        self.update_idletasks()

        data = get_city_weather(city)
        if not data:
            messagebox.showerror("Error", f"Could not find weather data for '{city}'. Please check the city name.")
            self.status_lbl.config(text="City not found.")
            return

        self.current_data = data
        self.render_data()
        self.status_lbl.config(text=f"Updated live from {data.get('provider', 'API')}")

    def toggle_unit(self):
        self.current_unit = "F" if self.current_unit == "C" else "C"
        self.unit_btn.config(text=f"°{self.current_unit}")
        if self.current_data:
            self.render_data()

    def render_data(self):
        d = self.current_data
        loc = f"{d['city']}, {d.get('country', '')}" if d.get('country') else d['city']
        self.loc_label.config(text=loc)
        self.condition_label.config(text=f"{d['icon']}  {d['condition']}")

        if self.current_unit == "C":
            self.temp_label.config(text=f"{d['temp_c']:.1f}°C")
            self.feels_label.config(text=f"Feels like {d['feels_like_c']:.1f}°C")
            self.wind_lbl.config(text=f"💨 Wind: {d['wind_speed_kmh']:.1f} km/h")
        else:
            self.temp_label.config(text=f"{d['temp_f']:.1f}°F")
            self.feels_label.config(text=f"Feels like {d['feels_like_f']:.1f}°F")
            self.wind_lbl.config(text=f"💨 Wind: {d['wind_speed_mph']:.1f} mph")

        self.hum_lbl.config(text=f"💧 Humidity: {d['humidity']}%")
        self.press_lbl.config(text=f"⏲️ Pressure: {d['pressure_hpa']} hPa")
        self.coords_lbl.config(text=f"📍 {d['latitude']:.2f}° N, {d['longitude']:.2f}° E")

        # Clear old forecast cards
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

        # Render 5 horizontal day cards
        forecast = d.get("forecast", [])
        for day in forecast:
            box = tk.Frame(self.forecast_frame, bg="#f8fafc", bd=1, relief=tk.SOLID, padx=6, pady=6)
            box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2)

            tk.Label(box, text=day["date"][5:], font=("Segoe UI", 9, "bold"), bg="#f8fafc", fg="#334155").pack()
            tk.Label(box, text=day.get("icon", "⛅"), font=("Segoe UI", 14), bg="#f8fafc").pack()

            if self.current_unit == "C":
                t_str = f"{day['temp_max_c']:.0f}° / {day['temp_min_c']:.0f}°"
            else:
                t_str = f"{day['temp_max_f']:.0f}° / {day['temp_min_f']:.0f}°"

            tk.Label(box, text=t_str, font=("Segoe UI", 8), bg="#f8fafc", fg="#1e293b").pack()
            tk.Label(box, text=f"🌧 {day.get('precip_prob', 0)}%", font=("Segoe UI", 7), bg="#f8fafc", fg="#64748b").pack()


def main():
    app = WeatherAppGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
