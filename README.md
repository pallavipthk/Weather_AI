<div align="center">

# 🌦️ WeatherSphere

### ✨ A magical, real-time weather experience ✨

*Live conditions, forecasts, air quality, and an interactive map, wrapped in weather-aware backgrounds and animated effects that change with the sky outside.*

☀️ **Current Weather** &nbsp;·&nbsp; 📅 **5-Day Forecast** &nbsp;·&nbsp; 🌬️ **Air Quality** &nbsp;·&nbsp; 🗺️ **Live Map** &nbsp;·&nbsp; 🌙 **Dark Mode**

</div>

---

## 🌈 Table of Contents

| | Section | | Section |
|---|---|---|---|
| 🌤️ | [About](#️-about) | ⚙️ | [Configuration](#️-configuration) |
| ✨ | [Features](#-features) | 🔌 | [Data Sources](#-data-sources) |
| 🎭 | [Weather Effects](#-weather-effects) | 🎨 | [Customisation](#-customisation) |
| 🧪 | [Tech Stack](#-tech-stack) | 🔒 | [Security Notes](#-security-notes) |
| 🧱 | [Project Structure](#-project-structure) | ⚠️ | [Known Limitations](#️-known-limitations) |
| 🚀 | [Getting Started](#-getting-started) | 🛠️ | [Troubleshooting](#️-troubleshooting) |
| 🧭 | [How to Use](#-how-to-use) | 🙏 | [Credits](#-credits) |

---

## 🌤️ About

**WeatherSphere** is a beautifully animated weather dashboard that turns raw forecast data into something you actually enjoy checking. Search any city or use your current location, and the whole page transforms: the background gradient shifts to match the conditions, and falling snow, rain, drifting clouds, glowing sun rays, glitter, or lightning flashes bring the weather to life.

Behind the magic is a clean, practical dashboard with everything you need to plan your day.

---

## ✨ Features

### 🌡️ Current Conditions
- 📍 Location name, country, and local time
- 🌡️ Large temperature display with a "feels like" reading
- 🖼️ Weather icon and plain-language condition
- 📊 Eight quick stats: wind speed, humidity, visibility, pressure, UV index, precipitation, cloud cover, and wind gust

### 📅 Forecasts
- 🗓️ **5-day forecast** with high and low temperatures, conditions, chance of rain, and max wind
- ⏰ **Hourly forecast** for the next 12 hours with temperature and rain chance

### 🌬️ Air Quality
- 🎚️ Simplified AQI badge with a Good, Moderate, or Poor rating
- 🧪 Individual readings for PM2.5, PM10, O₃, NO₂, SO₂, and CO

### 🌅 Sun Times
- 🌄 Sunrise and 🌇 sunset times for the selected location

### 🗺️ Interactive Weather Map
- 📌 Pan and zoom map that centres on the searched or detected location with a custom marker
- 🌙 Map tiles follow the dark and light theme

### 🚨 Weather Alerts
- ⚠️ Active alerts appear automatically with headline, description, and severity, and stay hidden when there are none

### 🔍 Search and Location
- 🏙️ Search any city or place by name, with Enter-key support
- 🧭 One-tap **My Location** using your browser's geolocation
- 🔄 Refresh button to pull the latest data
- 🛟 Graceful default to **Mumbai** if location access is denied

### 🌗 Look and Feel
- 🌙 Light and dark mode, remembered between visits
- 💎 Glassmorphism cards with soft blur and gradient accents
- 🫧 Floating particles, aurora glow, hover lifts, and button ripples
- 📱 Fully responsive for desktop, tablet, and mobile

---

## 🎭 Weather Effects

The scene reacts to the current condition:

| 🌍 Condition | 🎨 Background | 🎆 Effects |
|---|---|---|
| ☀️ Sunny / Clear | Warm sunrise gradient | Pulsing sun rays and glitter |
| ☁️ Cloudy | Soft grey-blue gradient | Drifting clouds and glitter |
| 🌧️ Rain / Drizzle | Deep blue and violet gradient | Falling raindrops and clouds |
| ⛈️ Thunderstorm | Dark stormy gradient | Rain, clouds, and lightning flashes |
| ❄️ Snow / Sleet / below 0°C | Cool pale gradient | Falling snowflakes and glitter |
| 🌌 Night / Other | Night or violet-pink gradient | Glitter and floating particles |

A gentle aurora glow and floating particles are always present in the background.

---

## 🧪 Tech Stack

| Layer | Technology |
|---|---|
| 🖥️ Frontend | HTML5, CSS3, vanilla JavaScript (single page) |
| 🐍 Backend | Python (`app.py`) |
| ☁️ Weather data | [WeatherAPI.com](https://www.weatherapi.com/) |
| 🗺️ Maps | [Leaflet](https://leafletjs.com/) 1.9.4 with OpenStreetMap tiles |
| 🔣 Icons | Font Awesome 6.4 |
| 🔤 Typography | Inter (Google Fonts) |

---

## 🧱 Project Structure

```
.
├── 🐍 app.py          Python application entry point
├── 🌐 index.html      Complete frontend: markup, styles, and logic
└── 📖 README.md       Project documentation
```

---

## 🚀 Getting Started

### 📋 Prerequisites
- 🌐 A modern web browser
- 🔑 A free API key from [WeatherAPI.com](https://www.weatherapi.com/)
- 🐍 Python 3 installed, if you want to run the project through `app.py`
- 📶 An internet connection, since weather data, map tiles, fonts, and icons load from online services

### 🛠️ Setup

1. 📥 Clone or download the repository
2. 🔑 Create a free account at WeatherAPI.com and copy your API key
3. ✏️ Open `index.html`, find the `API_KEY` constant near the top of the script section, and replace its value with your own key
4. 🚀 Launch the app using either option below

**Option A: open directly.** Double-click `index.html` to open it in your browser. All weather calls are made straight from the page.

**Option B: run with Python.** Start `app.py` from the project folder with Python and open the local address it prints in your terminal. Use this if `app.py` serves the page for you.

> 💡 Location detection works best over `http://localhost` or HTTPS, because browsers restrict geolocation on plain file pages and insecure sites.

---

## 🧭 How to Use

1. 🌍 On load, the app tries to detect your location and show local weather
2. 🔍 Type a city name in the search box and press **Enter** or click **Search**
3. 📍 Click **My Location** any time to jump back to where you are
4. 👀 Scroll through current conditions, the 5-day forecast, hourly outlook, air quality, sun times, and the map
5. 🔄 Use **Refresh** on the weather card to fetch the latest data
6. 🌙 Tap the moon or sun button to switch between dark and light themes

---

## ⚙️ Configuration

| 🔧 Setting | 📍 Where | 📝 Notes |
|---|---|---|
| Weather API key | `API_KEY` constant in `index.html` | Required for any weather data to load |
| Default city | The search box value and the fallback coordinates in `index.html` | Currently set to Mumbai |
| Forecast length | The `days` parameter in the forecast request | Currently 5 days |
| Hours shown | The hourly forecast loop in `updateHourlyForecast` | Currently the next 12 hours |

---

## 🔌 Data Sources

| 📡 Service | 🎯 Used for |
|---|---|
| WeatherAPI.com Search | Turning a typed city name into coordinates |
| WeatherAPI.com Current | Live conditions and air quality |
| WeatherAPI.com Forecast | 5-day outlook, hourly data, astronomy times, and alerts |
| OpenStreetMap tiles via Leaflet | The interactive map |
| Browser Geolocation | Detecting the user's position |

---

## 🎨 Customisation

| 🎯 Goal | 📍 What to change |
|---|---|
| Change brand colours | The CSS variables at the top of the stylesheet |
| Edit weather backgrounds | The `.bg-sunny`, `.bg-rainy`, and related gradient classes |
| Make effects lighter or heavier | The particle counts inside each `create...Effect` function |
| Add new condition effects | `updateWeatherEffects` and `updateBackground` |
| Change AQI thresholds | The AQI logic inside `updateAirQuality` |
| Switch map style | The tile layer URL in `initMap` |
| Rename the app | The title, header text, and footer in `index.html` |

---

## 🔒 Security Notes

- 🔑 **Do not publish a real API key.** Anything placed in `index.html` is visible to every visitor. Use your own key, restrict it in your WeatherAPI dashboard where possible, and rotate it if it has been shared publicly.
- 🛡️ For a production deployment, route weather requests through your backend (`app.py`) so the key stays on the server.
- 📍 Location access is requested only when you use the location feature, and coordinates are used only to fetch weather.

---

## ⚠️ Known Limitations

- 🌬️ The AQI badge is a **simplified indicator** based on raw pollutant readings and is not the official AQI of any country
- ⏰ The hourly list starts from the viewer's current hour rather than the searched city's local hour, so it can be offset for far-away locations
- 🌅 The sunrise and sunset icons use Font Awesome names that may not be included in the free icon set and may not display
- 📶 Needs an internet connection and valid API key to function
- 🖥️ Heavy animations can be demanding on low-end devices
- 📅 The footer copyright year is hard-coded to 2024

---

## 🛠️ Troubleshooting

| 🌧️ Problem | 🌈 Fix |
|---|---|
| Page stays on "Loading weather magic..." | Check that your API key is valid and has not exceeded its quota, and open the browser console for errors |
| "City not found" message | Try a different spelling or add the country name |
| Location button does nothing or shows Mumbai | Allow location permission in your browser, and use localhost or HTTPS |
| Map is blank | Check your internet connection and that Leaflet loaded correctly |
| No alerts shown | Alerts only appear when the API reports an active warning for that area |
| Effects feel slow | Reduce the particle counts in the effect functions |

---

## 🙏 Credits

- ☁️ Weather and air quality data by [WeatherAPI.com](https://www.weatherapi.com/)
- 🗺️ Mapping by [Leaflet](https://leafletjs.com/) and © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors
- 🔣 Icons by [Font Awesome](https://fontawesome.com/)
- 🔤 Typography by [Inter](https://rsms.me/inter/) via Google Fonts

---

## 📄 License

No license has been specified for this project. All rights are reserved by the author. If you would like to use or redistribute this code, please contact the author first.

---

<div align="center">

🌈 **Whatever the weather, make it magical.** 🌈

</div>
