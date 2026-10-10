"""The practice weather server of Project 12.

It answers the two Open-Meteo endpoints that the project uses, in the same
JSON format as the real service, with made-up sample weather for three
cities (Lisbon, Oslo and Chicago). None of its numbers are real
observations. Run it in a terminal of its own and leave it running while you
work on the project; press Ctrl+C to stop it:

    python practice_server.py

It listens only on your own computer, at http://127.0.0.1:8110.
"""
import json
import threading
from datetime import date, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

FIRST_DAY = date(2026, 10, 12)
CITIES = {  # made-up sample weather: (code, max, min, rain) per day
    "lisbon": {"name": "Lisbon", "latitude": 38.71667,
               "longitude": -9.13333, "elevation": 45.0,
               "country_code": "PT", "timezone": "Europe/Lisbon",
               "country": "Portugal", "admin1": "Lisbon",
               "grid": [38.7, -9.125], "tz": ["GMT+1", 3600],
               "now": [21.4, 64, 14.8, 2],
               "days": [[2, 23.1, 15.2, 0.0], [3, 21.8, 15.9, 0.2],
                        [61, 19.4, 15.1, 4.6], [63, 18.2, 14.0, 11.3],
                        [80, 19.0, 13.6, 2.1], [1, 21.5, 13.8, 0.0],
                        [0, 23.4, 14.9, 0.0]]},
    "oslo": {"name": "Oslo", "latitude": 59.91273, "longitude": 10.74609,
             "elevation": 26.0, "country_code": "NO",
             "timezone": "Europe/Oslo", "country": "Norway",
             "admin1": "Oslo", "grid": [59.9, 10.75], "tz": ["GMT+2", 7200],
             "now": [7.9, 81, 11.2, 3],
             "days": [[3, 9.8, 4.1, 0.4], [51, 8.6, 3.9, 1.2],
                      [45, 7.2, 1.8, 0.0], [1, 10.1, 0.6, 0.0],
                      [0, 11.3, 1.9, 0.0], [71, 4.2, -1.3, 2.8],
                      [73, 2.1, -3.4, 6.5]]},
    "chicago": {"name": "Chicago", "latitude": 41.85003,
                "longitude": -87.65005, "elevation": 179.0,
                "country_code": "US", "timezone": "America/Chicago",
                "country": "United States", "admin1": "Illinois",
                "grid": [41.875, -87.625], "tz": ["GMT-5", -18000],
                "now": [16.1, 58, 22.3, 1],
                "days": [[1, 18.9, 9.4, 0.0], [95, 21.7, 12.2, 18.4],
                         [81, 15.3, 8.1, 6.2], [3, 12.4, 5.6, 0.0],
                         [2, 14.8, 4.9, 0.0], [0, 17.6, 7.3, 0.0],
                         [61, 13.2, 8.8, 3.9]]},
}
PLACE_KEYS = ["name", "latitude", "longitude", "elevation", "country_code",
              "timezone", "country", "admin1"]


def search(q):
    """The geocoding endpoint: /v1/search?name=...&count=..."""
    city = CITIES.get(q.get("name", "").strip().lower())
    if city is None:                      # the real API: no "results" key
        return 200, {"generationtime_ms": 0.4}
    place = {"id": 1 + list(CITIES).index(city["name"].lower())}
    place |= {key: city[key] for key in PLACE_KEYS}
    return 200, {"results": [place], "generationtime_ms": 0.6}


def find_city(lat, lon):
    for city in CITIES.values():
        if abs(city["latitude"] - lat) + abs(city["longitude"] - lon) < 0.2:
            return city
    return None


def forecast(q):
    """The forecast endpoint: /v1/forecast?latitude=...&longitude=..."""
    try:
        lat, lon = float(q["latitude"]), float(q["longitude"])
    except (KeyError, ValueError):
        return 400, {"error": True, "reason": "Parameters 'latitude' and "
                     "'longitude' are required numbers."}
    if not -90 <= lat <= 90:
        return 400, {"error": True, "reason": "Latitude must be in range "
                     f"of -90 to 90°. Given: {lat}."}
    city = find_city(lat, lon)
    if city is None:
        return 400, {"error": True, "reason": "The practice server only "
                     "has sample data for Lisbon, Oslo and Chicago."}
    fahrenheit = q.get("temperature_unit") == "fahrenheit"
    mph = q.get("wind_speed_unit") == "mph"

    def temp(c):
        return round(c * 9 / 5 + 32, 1) if fahrenheit else c

    def wind(kmh):
        return round(kmh / 1.609344, 1) if mph else kmh

    t_unit, w_unit = ("°F" if fahrenheit else "°C"), ("mp/h" if mph
                                                     else "km/h")
    t, humidity, w, code = city["now"]
    now_values = {"temperature_2m": (temp(t), t_unit),
                  "relative_humidity_2m": (humidity, "%"),
                  "wind_speed_10m": (wind(w), w_unit),
                  "weather_code": (code, "wmo code")}
    n_days = min(int(q.get("forecast_days", 7)), 7)
    days = city["days"][:n_days]
    day_values = {
        "weather_code": ([d[0] for d in days], "wmo code"),
        "temperature_2m_max": ([temp(d[1]) for d in days], t_unit),
        "temperature_2m_min": ([temp(d[2]) for d in days], t_unit),
        "precipitation_sum": ([d[3] for d in days], "mm")}
    body = {"latitude": city["grid"][0], "longitude": city["grid"][1],
            "generationtime_ms": 0.05,
            "utc_offset_seconds": city["tz"][1],
            "timezone": city["timezone"],
            "timezone_abbreviation": city["tz"][0],
            "elevation": city["elevation"]}
    wanted = [v for v in q.get("current", "").split(",") if v]
    if wanted:
        body["current_units"] = {"time": "iso8601", "interval": "seconds"}
        body["current"] = {"time": f"{FIRST_DAY}T14:00", "interval": 900}
        for name in wanted:
            value, unit = now_values[name]
            body["current_units"][name] = unit
            body["current"][name] = value
    wanted = [v for v in q.get("daily", "").split(",") if v]
    if wanted:
        dates = [str(FIRST_DAY + timedelta(days=i)) for i in range(n_days)]
        body["daily_units"] = {"time": "iso8601"}
        body["daily"] = {"time": dates}
        for name in wanted:
            values, unit = day_values[name]
            body["daily_units"][name] = unit
            body["daily"][name] = values
    return 200, body


ROUTES = {"/v1/search": search, "/v1/forecast": forecast}


class WeatherHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlsplit(self.path)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        route = ROUTES.get(url.path)
        if route is None:
            status, body = 404, {"error": True, "reason": "Not Found"}
        else:
            status, body = route(q)
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass                           # keep the terminal quiet


def start(port=8110):
    """Start the server in a background thread and return it."""
    server = ThreadingHTTPServer(("127.0.0.1", port), WeatherHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8110), WeatherHandler)
    print("Practice weather server at http://127.0.0.1:8110 "
          "(Ctrl+C stops it)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopped.")
