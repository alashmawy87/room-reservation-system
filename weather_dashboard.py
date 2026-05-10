import requests
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import threading


class WeatherAPI:
    """Fetches weather data from Open-Meteo API (free, no key required)"""
    
    def __init__(self):
        # Using Open-Meteo API - free and no API key needed
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    
    def search_location(self, city_name):
        """Search for a city and get coordinates"""
        try:
            params = {
                "name": city_name,
                "count": 1,
                "language": "en",
                "format": "json"
            }
            response = requests.get(self.geocoding_url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            if data.get("results"):
                result = data["results"][0]
                return {
                    "name": result.get("name"),
                    "country": result.get("country"),
                    "latitude": result.get("latitude"),
                    "longitude": result.get("longitude"),
                    "timezone": result.get("timezone")
                }
            return None
        except Exception as e:
            print(f"Error searching location: {e}")
            return None
    
    def get_current_weather(self, latitude, longitude, timezone):
        """Get current weather data"""
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m",
                "hourly": "temperature_2m,precipitation,weather_code",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
                "timezone": timezone,
                "temperature_unit": "celsius"
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None
    
    def interpret_weather_code(self, code):
        """Convert WMO weather code to description"""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy (rime)",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(code, "Unknown")
    
    def get_weather_emoji(self, code):
        """Get emoji for weather code"""
        emojis = {
            0: "☀️",
            1: "🌤️",
            2: "⛅",
            3: "☁️",
            45: "🌫️",
            48: "🌫️",
            51: "🌦️",
            53: "🌧️",
            55: "🌧️",
            61: "🌧️",
            63: "⛈️",
            65: "⛈️",
            71: "❄️",
            73: "❄️",
            75: "❄️",
            80: "🌧️",
            81: "⛈️",
            82: "⛈️",
            95: "⛈️",
            96: "⛈️",
            99: "⛈️"
        }
        return emojis.get(code, "🌡️")


class WeatherDashboard:
    """GUI Dashboard for weather display"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1a1a1a")
        
        self.api = WeatherAPI()
        self.current_location = None
        self.weather_data = None
        
        # Styles
        self.bg_color = "#1a1a1a"
        self.fg_color = "#ffffff"
        self.accent_color = "#3498db"
        
        self.create_ui()
    
    def create_ui(self):
        """Create the user interface"""
        # Top search bar
        search_frame = tk.Frame(self.root, bg="#2a2a2a")
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            search_frame,
            text="Search City:",
            font=("Arial", 12),
            fg=self.fg_color,
            bg="#2a2a2a"
        ).pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 12),
            width=30,
            bg="#333333",
            fg=self.fg_color,
            insertbackground=self.fg_color
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search_weather())
        
        tk.Button(
            search_frame,
            text="Search",
            font=("Arial", 11, "bold"),
            bg=self.accent_color,
            fg="white",
            command=self.search_weather
        ).pack(side=tk.LEFT, padx=5)
        
        # Main content
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Current weather section
        self.current_frame = tk.Frame(self.main_frame, bg="#2a2a2a", relief=tk.RAISED, bd=2)
        self.current_frame.pack(fill=tk.X, pady=10)
        
        self.location_label = tk.Label(
            self.current_frame,
            text="Select a city to view weather",
            font=("Arial", 24, "bold"),
            fg=self.accent_color,
            bg="#2a2a2a"
        )
        self.location_label.pack(pady=10)
        
        # Weather details grid
        details_frame = tk.Frame(self.current_frame, bg="#2a2a2a")
        details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Temperature
        self.temp_label = tk.Label(
            details_frame,
            text="--°C",
            font=("Arial", 72, "bold"),
            fg=self.accent_color,
            bg="#2a2a2a"
        )
        self.temp_label.grid(row=0, column=0, sticky="w", padx=20)
        
        # Weather icon and description
        weather_info = tk.Frame(details_frame, bg="#2a2a2a")
        weather_info.grid(row=0, column=1, sticky="ew", padx=20)
        
        self.weather_emoji = tk.Label(
            weather_info,
            text="🌡️",
            font=("Arial", 48),
            bg="#2a2a2a"
        )
        self.weather_emoji.pack()
        
        self.weather_desc = tk.Label(
            weather_info,
            text="--",
            font=("Arial", 14),
            fg=self.fg_color,
            bg="#2a2a2a"
        )
        self.weather_desc.pack()
        
        # Additional info
        info_frame = tk.Frame(details_frame, bg="#2a2a2a")
        info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=20)
        
        self.details_text = tk.Label(
            info_frame,
            text="",
            font=("Arial", 11),
            fg=self.fg_color,
            bg="#2a2a2a",
            justify=tk.LEFT
        )
        self.details_text.pack(anchor="w")
        
        # Hourly forecast
        forecast_label = tk.Label(
            self.main_frame,
            text="24-Hour Forecast",
            font=("Arial", 16, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        forecast_label.pack(anchor="w", pady=(20, 10))
        
        self.hourly_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.hourly_frame.pack(fill=tk.BOTH, expand=True)
        
        # Daily forecast
        daily_label = tk.Label(
            self.main_frame,
            text="7-Day Forecast",
            font=("Arial", 16, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        daily_label.pack(anchor="w", pady=(20, 10))
        
        self.daily_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.daily_frame.pack(fill=tk.BOTH, expand=True)
    
    def search_weather(self):
        """Search for weather in a city"""
        city = self.search_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        # Search in background thread
        thread = threading.Thread(target=self._fetch_weather, args=(city,))
        thread.daemon = True
        thread.start()
    
    def _fetch_weather(self, city):
        """Fetch weather data in background"""
        # Search location
        location = self.api.search_location(city)
        if not location:
            self.root.after(0, lambda: messagebox.showerror("Error", f"City '{city}' not found"))
            return
        
        # Get weather
        weather = self.api.get_current_weather(
            location["latitude"],
            location["longitude"],
            location["timezone"]
        )
        
        if not weather:
            self.root.after(0, lambda: messagebox.showerror("Error", "Failed to fetch weather"))
            return
        
        self.current_location = location
        self.weather_data = weather
        
        # Update UI in main thread
        self.root.after(0, self.update_display)
    
    def update_display(self):
        """Update the dashboard display"""
        if not self.current_location or not self.weather_data:
            return
        
        loc = self.current_location
        data = self.weather_data
        current = data.get("current", {})
        daily = data.get("daily", {})
        hourly = data.get("hourly", {})
        
        # Update location
        location_text = f"{loc['name']}, {loc['country']}"
        self.location_label.config(text=location_text)
        
        # Update current weather
        temp = current.get("temperature_2m", "--")
        feels_like = current.get("apparent_temperature", "--")
        humidity = current.get("relative_humidity_2m", "--")
        wind_speed = current.get("wind_speed_10m", "--")
        precipitation = current.get("precipitation", 0)
        weather_code = current.get("weather_code", 0)
        
        self.temp_label.config(text=f"{temp}°C")
        
        weather_desc = self.api.interpret_weather_code(weather_code)
        emoji = self.api.get_weather_emoji(weather_code)
        
        self.weather_emoji.config(text=emoji)
        self.weather_desc.config(text=weather_desc)
        
        details = f"""
Feels Like: {feels_like}°C
Humidity: {humidity}%
Wind Speed: {wind_speed} km/h
Precipitation: {precipitation} mm
        """
        self.details_text.config(text=details.strip())
        
        # Update hourly forecast
        self._update_hourly_forecast(hourly, daily)
        
        # Update daily forecast
        self._update_daily_forecast(daily)
    
    def _update_hourly_forecast(self, hourly, daily):
        """Update hourly forecast display"""
        for widget in self.hourly_frame.winfo_children():
            widget.destroy()
        
        hourly_frame = tk.Frame(self.hourly_frame, bg="#2a2a2a")
        hourly_frame.pack(fill=tk.BOTH, expand=True)
        
        times = hourly.get("time", [])[:24]
        temps = hourly.get("temperature_2m", [])[:24]
        codes = hourly.get("weather_code", [])[:24]
        
        for i, (time, temp, code) in enumerate(zip(times, temps, codes)):
            hour = datetime.fromisoformat(time).strftime("%H:%M")
            emoji = self.api.get_weather_emoji(code)
            
            item = tk.Frame(hourly_frame, bg="#333333")
            item.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
            
            tk.Label(item, text=hour, font=("Arial", 9), fg=self.fg_color, bg="#333333").pack()
            tk.Label(item, text=emoji, font=("Arial", 24), bg="#333333").pack()
            tk.Label(item, text=f"{temp}°C", font=("Arial", 10, "bold"), fg=self.accent_color, bg="#333333").pack()
    
    def _update_daily_forecast(self, daily):
        """Update daily forecast display"""
        for widget in self.daily_frame.winfo_children():
            widget.destroy()
        
        daily_frame = tk.Frame(self.daily_frame, bg="#2a2a2a")
        daily_frame.pack(fill=tk.BOTH, expand=True)
        
        dates = daily.get("time", [])[:7]
        temps_max = daily.get("temperature_2m_max", [])[:7]
        temps_min = daily.get("temperature_2m_min", [])[:7]
        codes = daily.get("weather_code", [])[:7]
        
        for date, temp_max, temp_min, code in zip(dates, temps_max, temps_min, codes):
            day = datetime.fromisoformat(date).strftime("%a, %b %d")
            emoji = self.api.get_weather_emoji(code)
            desc = self.api.interpret_weather_code(code)
            
            item = tk.Frame(daily_frame, bg="#333333", relief=tk.RAISED, bd=1)
            item.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
            
            tk.Label(item, text=day, font=("Arial", 10, "bold"), fg=self.accent_color, bg="#333333").pack()
            tk.Label(item, text=emoji, font=("Arial", 32), bg="#333333").pack()
            tk.Label(item, text=desc, font=("Arial", 9), fg=self.fg_color, bg="#333333").pack()
            tk.Label(item, text=f"{temp_max}°C / {temp_min}°C", font=("Arial", 9), fg=self.accent_color, bg="#333333").pack()


def main():
    """Main entry point"""
    root = tk.Tk()
    dashboard = WeatherDashboard(root)
    
    # Load default city
    root.after(500, lambda: [
        dashboard.search_entry.insert(0, "London"),
        dashboard.search_weather()
    ])
    
    root.mainloop()


if __name__ == "__main__":
    main()
