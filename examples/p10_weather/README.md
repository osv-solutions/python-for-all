# Project 10: practice server and sample forecast

`practice_server.py` plays the part of the two Open-Meteo endpoints that the
weather dashboard uses, `/v1/search` (geocoding) and `/v1/forecast`, in the
same JSON format as the real service. Its weather for Lisbon, Oslo and
Chicago is made-up sample data, not real observations. It uses only the
standard library and listens only on your own computer. Start it in a
terminal of its own and leave it running:

```bash
cd examples/p10_weather
python practice_server.py
```

Its address is `http://127.0.0.1:8110`; press Ctrl+C to stop it. The
project's script in `projects/` starts its own copy, so you don't need this
one to run that script.

`sample_forecast.json` is the saved forecast that the dashboard shows when
there is no connection: one cache entry for Lisbon, made by the program from
the practice server. Copy it next to your own program.

To get live weather instead, set `GEO_URL` and `FORECAST_URL` in the program
to the real addresses given in the book. Open-Meteo is free for
non-commercial use and needs no API key.
