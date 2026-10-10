"""Project 12 (Advanced): Weather Dashboard from a Web API

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p12_weather.py

or open the notebook and run the cells in order.
"""

# %% Step 1: Two APIs and a practice server
# Setup: recreates the context this solution builds on (not printed in the book).
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


server = start()

# %% Step 1: Two APIs and a practice server
from dataclasses import dataclass
from datetime import date, datetime, timedelta

import requests

GEO_URL = "http://127.0.0.1:8110/v1/search"
FORECAST_URL = "http://127.0.0.1:8110/v1/forecast"
# The real service, free for non-commercial use:
# GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
# FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
AGENT = {"User-Agent": "ada-weather/1.0 (ada@example.com)"}

# %% Step 1: Two APIs and a practice server
type Params = dict[str, str | int | float]


class WeatherError(Exception):
    """A problem to report to the user in plain words."""


def fetch_json(url: str, params: Params) -> dict:
    """GET a URL with a query string and return its JSON body."""
    r = requests.get(url, params=params, headers=AGENT, timeout=10)
    if r.status_code != 200:
        reason = r.json().get("reason", r.reason)
        raise WeatherError(f"service error {r.status_code}: {reason}")
    return r.json()

# %% Step 1: Two APIs and a practice server
try:
    fetch_json(FORECAST_URL, {"latitude": 91, "longitude": 0})
except WeatherError as err:
    print(err)

# %% Step 2: From a city name to coordinates
@dataclass
class Place:
    name: str
    country: str
    latitude: float
    longitude: float


def find_place(city: str) -> Place:
    data = fetch_json(GEO_URL, {"name": city, "count": 1})
    if "results" not in data:            # the API found nothing
        raise WeatherError(f"no place called {city!r}")
    top = data["results"][0]
    return Place(top["name"], top["country"],
                 top["latitude"], top["longitude"])

# %% Step 2: From a city name to coordinates
place = find_place("lisbon")
print(place.name, place.country, place.latitude, place.longitude)
try:
    find_place("Atlantis")
except WeatherError as err:
    print(err)

# %% Step 3: The forecast as data classes
CURRENT = ("temperature_2m,relative_humidity_2m,"
           "wind_speed_10m,weather_code")
DAILY = ("weather_code,temperature_2m_max,temperature_2m_min,"
         "precipitation_sum")


def get_forecast(place: Place, unit: str = "celsius") -> dict:
    params: Params = {
        "latitude": place.latitude, "longitude": place.longitude,
        "current": CURRENT, "daily": DAILY,
        "timezone": "auto", "forecast_days": 7}
    if unit == "fahrenheit":
        params.update(temperature_unit="fahrenheit",
                      wind_speed_unit="mph")
    return fetch_json(FORECAST_URL, params)

# %% Step 3: The forecast as data classes
data = get_forecast(find_place("Lisbon"))
for name, values in data["daily"].items():
    print(f"{name:>18}: {values[:2]} ...")

# %% Step 3: The forecast as data classes
@dataclass
class Current:
    time: str
    temperature: float
    humidity: int
    wind: float
    code: int


@dataclass
class DayForecast:
    day: date
    code: int
    high: float
    low: float
    rain: float

# %% Step 3: The forecast as data classes
def parse_current(data: dict) -> Current:
    c = data["current"]
    return Current(c["time"], c["temperature_2m"],
                   c["relative_humidity_2m"], c["wind_speed_10m"],
                   c["weather_code"])


def parse_days(data: dict) -> list[DayForecast]:
    d = data["daily"]
    rows = zip(d["time"], d["weather_code"], d["temperature_2m_max"],
               d["temperature_2m_min"], d["precipitation_sum"])
    return [DayForecast(date.fromisoformat(t), code, high, low, rain)
            for t, code, high, low, rain in rows]


days = parse_days(data)
print(len(days), days[0].day, days[0].high, days[-1].day)

# %% Step 4: Weather codes and the dashboard
WEATHER = [(0, "()", "Clear sky"), (1, "()", "Mainly clear"),
           (2, "(~", "Partly cloudy"), (3, "~~", "Overcast"),
           (48, "==", "Fog"), (57, ",,", "Drizzle"),
           (67, "//", "Rain"), (77, "**", "Snow"),
           (82, "//", "Rain showers"), (86, "**", "Snow showers"),
           (99, "!!", "Thunderstorm")]


def describe(code: int) -> str:
    for top, picture, words in WEATHER:
        if code <= top:
            return f"{picture} {words}"
    return f"?? code {code}"


print([describe(code) for code in (2, 63, 95, 120)])

# %% Step 4: Weather codes and the dashboard
def bar(low: float, high: float, bottom: float, top: float,
        width: int = 24) -> str:
    """Draw low..high as '=' on a scale from bottom to top."""
    step = (top - bottom) / (width - 1)   # degrees per character
    start = round((low - bottom) / step)
    end = round((high - bottom) / step)
    return ("." * start + "=" * (end - start + 1)
            + "." * (width - 1 - end))


print(bar(10, 20, 10, 30), bar(20, 30, 10, 30), bar(18, 19, 10, 30))

# %% Step 4: Weather codes and the dashboard
def show(place: Place, data: dict, note: str) -> None:
    now, units = parse_current(data), data["current_units"]
    print(f"{place.name}, {place.country}".upper())
    print(note)
    print(f"Now ({now.time[-5:]})  {now.temperature:.0f}"
          f"{units['temperature_2m']}  {describe(now.code)}  "
          f"humidity {now.humidity}%  wind {now.wind:.0f} "
          f"{units['wind_speed_10m']}")
    days = parse_days(data)
    bottom = min(day.low for day in days)
    top = max(day.high for day in days)
    for day in days:
        chart = bar(day.low, day.high, bottom, top)
        print(f"{day.day:%a %d}  {describe(day.code):<16} "
              f"{day.low:>4.0f}° {chart} {day.high:>3.0f}°  "
              f"{day.rain:>4.1f} mm")

# %% Step 4: Weather codes and the dashboard
place = find_place("Oslo")
show(place, get_forecast(place), "Live from the weather service")

# %% Step 5: A cache file
import json
from dataclasses import asdict
from pathlib import Path

CACHE = Path("weather_cache.json")
MAX_AGE = timedelta(minutes=30)


def fetch_entry(city: str, unit: str, now: datetime) -> dict:
    print(f"(asking the API about {city})")
    place = find_place(city)
    return {"saved_at": now.isoformat(timespec="minutes"),
            "place": asdict(place),
            "forecast": get_forecast(place, unit)}

# %% Step 5: A cache file
# Setup: recreates the context this solution builds on (not printed in the book).
CACHE.unlink(missing_ok=True)       # start every run with no cache

# %% Step 5: A cache file
def weather(city: str, unit: str, now: datetime) -> tuple[dict, str]:
    key = f"{city.strip().lower()}|{unit}"
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    entry = cache.get(key)
    if entry:
        saved = datetime.fromisoformat(entry["saved_at"])
        if now - saved < MAX_AGE:
            return entry, "cache"
    entry = fetch_entry(city, unit, now)
    cache[key] = entry
    CACHE.write_text(json.dumps(cache, indent=2))
    return entry, "live"

# %% Step 5: A cache file
NOW = datetime(2026, 10, 12, 14, 5)
for minutes in [0, 10, 45]:
    when = NOW + timedelta(minutes=minutes)
    entry, source = weather("Lisbon", "celsius", when)
    print(f"{when:%H:%M} {source:<5} saved at {entry['saved_at']}")

# %% Step 6: When the network fails
SAMPLE = Path("sample_forecast.json")
entry = fetch_entry("Lisbon", "celsius", NOW)
SAMPLE.write_text(json.dumps(entry, indent=2))

# %% Step 6: When the network fails
def weather_or_sample(city: str, unit: str,
                      now: datetime) -> tuple[dict, str]:
    try:
        return weather(city, unit, now)
    except (requests.ConnectionError, requests.Timeout):
        return json.loads(SAMPLE.read_text()), "sample"

# %% Step 7: Putting it together
NOTES = {"live": "Live from the weather service",
         "cache": "From the cache, saved {saved}",
         "sample": "OFFLINE: showing a sample saved {saved}"}


def dashboard(city: str, unit: str = "celsius",
              now: datetime | None = None) -> None:
    now = now or datetime.now()
    try:
        entry, source = weather_or_sample(city, unit, now)
    except WeatherError as err:
        print("Sorry:", err)
        return
    note = NOTES[source].format(saved=entry["saved_at"])
    show(Place(**entry["place"]), entry["forecast"], note)

# %% Step 7: Putting it together
dashboard("Chicago", "fahrenheit", now=NOW)
dashboard("Olso", now=NOW)

# %% Step 7: Putting it together
GEO_URL = "http://127.0.0.1:8199/v1/search"     # nothing listens here
dashboard("Oslo", now=NOW)
GEO_URL = "http://127.0.0.1:8110/v1/search"     # the server again

# %% Step 7: Putting it together
# Setup: recreates the context this solution builds on (not printed in the book).
server.shutdown()
server.server_close()
