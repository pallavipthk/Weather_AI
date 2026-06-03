# weather_backend.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import requests
import json
from functools import wraps
import time
import logging

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration
WEATHER_API_KEY = "4c34d3c05953498597045819252112"
WEATHER_API_URL = "http://api.weatherapi.com/v1"

# Simple cache
cache = {}
CACHE_TIMEOUT = 300  # 5 minutes

def cached(timeout=CACHE_TIMEOUT):
    """Decorator for caching API responses"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            if cache_key in cache:
                cached_data, timestamp = cache[cache_key]
                if time.time() - timestamp < timeout:
                    return cached_data
            result = func(*args, **kwargs)
            cache[cache_key] = (result, time.time())
            return result
        return wrapper
    return decorator

def make_api_request(endpoint, params):
    """Make API request to WeatherAPI"""
    params['key'] = WEATHER_API_KEY
    url = f"{WEATHER_API_URL}/{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {str(e)}")
        return {'error': str(e)}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'message': 'Weather API is running'
    })

@app.route('/api/weather/current', methods=['GET'])
@cached(timeout=300)
def get_current_weather():
    """
    Get current weather for any city, state, or country
    Examples:
    - /api/weather/current?city=Mumbai
    - /api/weather/current?city=California
    - /api/weather/current?city=New York
    - /api/weather/current?lat=19.0760&lon=72.8777
    """
    city = request.args.get('city')
    state = request.args.get('state')
    country = request.args.get('country')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    # Build query string
    if lat and lon:
        query = f"{lat},{lon}"
    elif city and state and country:
        query = f"{city},{state},{country}"
    elif city and state:
        query = f"{city},{state}"
    elif city:
        query = city
    else:
        return jsonify({'error': 'Please provide city, state, country, or coordinates'}), 400
    
    result = make_api_request('current.json', {'q': query, 'aqi': 'yes'})
    
    if 'error' in result:
        return jsonify({'error': result['error']['message']}), 404
    
    return jsonify({
        'location': {
            'name': result['location']['name'],
            'region': result['location'].get('region', ''),
            'country': result['location']['country'],
            'localtime': result['location']['localtime'],
            'lat': result['location']['lat'],
            'lon': result['location']['lon']
        },
        'current': {
            'temp_c': result['current']['temp_c'],
            'temp_f': result['current']['temp_f'],
            'condition': result['current']['condition']['text'],
            'condition_icon': result['current']['condition']['icon'],
            'wind_kph': result['current']['wind_kph'],
            'wind_dir': result['current']['wind_dir'],
            'humidity': result['current']['humidity'],
            'pressure_mb': result['current']['pressure_mb'],
            'feelslike_c': result['current']['feelslike_c'],
            'vis_km': result['current']['vis_km'],
            'uv': result['current']['uv'],
            'gust_kph': result['current'].get('gust_kph', 0),
            'cloud': result['current']['cloud'],
            'precip_mm': result['current']['precip_mm']
        },
        'air_quality': result['current'].get('air_quality', {})
    })

@app.route('/api/weather/forecast', methods=['GET'])
@cached(timeout=300)
def get_forecast():
    """
    Get weather forecast for any city, state, or country
    Examples:
    - /api/weather/forecast?city=Mumbai&days=5
    - /api/weather/forecast?city=California&days=3
    - /api/weather/forecast?city=New York&days=7
    """
    city = request.args.get('city')
    state = request.args.get('state')
    country = request.args.get('country')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    days = request.args.get('days', 5, type=int)
    
    # Build query string
    if lat and lon:
        query = f"{lat},{lon}"
    elif city and state and country:
        query = f"{city},{state},{country}"
    elif city and state:
        query = f"{city},{state}"
    elif city:
        query = city
    else:
        return jsonify({'error': 'Please provide city, state, country, or coordinates'}), 400
    
    days = min(days, 10)  # Max 10 days
    
    result = make_api_request('forecast.json', {
        'q': query, 
        'days': days, 
        'aqi': 'yes',
        'alerts': 'yes'
    })
    
    if 'error' in result:
        return jsonify({'error': result['error']['message']}), 404
    
    forecast_data = []
    for day in result['forecast']['forecastday']:
        forecast_data.append({
            'date': day['date'],
            'max_temp_c': day['day']['maxtemp_c'],
            'min_temp_c': day['day']['mintemp_c'],
            'avg_temp_c': day['day']['avgtemp_c'],
            'condition': day['day']['condition']['text'],
            'condition_icon': day['day']['condition']['icon'],
            'rain_chance': day['day']['daily_chance_of_rain'],
            'snow_chance': day['day']['daily_chance_of_snow'],
            'wind_kph': day['day']['maxwind_kph'],
            'humidity': day['day']['avghumidity'],
            'uv': day['day']['uv'],
            'sunrise': day['astro']['sunrise'],
            'sunset': day['astro']['sunset'],
            'moon_phase': day['astro']['moon_phase']
        })
    
    return jsonify({
        'location': {
            'name': result['location']['name'],
            'region': result['location'].get('region', ''),
            'country': result['location']['country'],
            'localtime': result['location']['localtime']
        },
        'forecast': forecast_data,
        'alerts': result.get('alerts', {}).get('alert', [])
    })

@app.route('/api/weather/hourly', methods=['GET'])
@cached(timeout=180)
def get_hourly():
    """
    Get hourly forecast for any city, state, or country
    Examples:
    - /api/weather/hourly?city=Mumbai&hours=12
    - /api/weather/hourly?city=California&hours=24
    """
    city = request.args.get('city')
    state = request.args.get('state')
    country = request.args.get('country')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    hours = request.args.get('hours', 12, type=int)
    
    # Build query string
    if lat and lon:
        query = f"{lat},{lon}"
    elif city and state and country:
        query = f"{city},{state},{country}"
    elif city and state:
        query = f"{city},{state}"
    elif city:
        query = city
    else:
        return jsonify({'error': 'Please provide city, state, country, or coordinates'}), 400
    
    hours = min(hours, 48)  # Max 48 hours
    
    result = make_api_request('forecast.json', {'q': query, 'days': 2, 'aqi': 'yes'})
    
    if 'error' in result:
        return jsonify({'error': result['error']['message']}), 404
    
    hourly_data = []
    for day in result['forecast']['forecastday']:
        for hour in day['hour'][:hours]:
            time_obj = datetime.fromisoformat(hour['time'].replace(' ', 'T'))
            hourly_data.append({
                'time': hour['time'],
                'hour': time_obj.strftime('%I %p'),
                'temp_c': hour['temp_c'],
                'condition': hour['condition']['text'],
                'condition_icon': hour['condition']['icon'],
                'rain_chance': hour['chance_of_rain'],
                'snow_chance': hour['chance_of_snow'],
                'wind_kph': hour['wind_kph'],
                'humidity': hour['humidity'],
                'feelslike_c': hour['feelslike_c']
            })
    
    return jsonify({
        'location': {
            'name': result['location']['name'],
            'region': result['location'].get('region', ''),
            'country': result['location']['country']
        },
        'hourly': hourly_data[:hours]
    })

@app.route('/api/weather/air-quality', methods=['GET'])
@cached(timeout=300)
def get_air_quality():
    """
    Get air quality data for any city, state, or country
    Examples:
    - /api/weather/air-quality?city=Mumbai
    - /api/weather/air-quality?city=Delhi
    """
    city = request.args.get('city')
    state = request.args.get('state')
    country = request.args.get('country')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    # Build query string
    if lat and lon:
        query = f"{lat},{lon}"
    elif city and state and country:
        query = f"{city},{state},{country}"
    elif city and state:
        query = f"{city},{state}"
    elif city:
        query = city
    else:
        return jsonify({'error': 'Please provide city, state, country, or coordinates'}), 400
    
    result = make_api_request('current.json', {'q': query, 'aqi': 'yes'})
    
    if 'error' in result:
        return jsonify({'error': result['error']['message']}), 404
    
    aqi_data = result['current'].get('air_quality', {})
    
    # Calculate AQI level
    pm25 = aqi_data.get('pm2_5', 0)
    if pm25 <= 50:
        aqi_level = 'Good'
        aqi_color = '#10B981'
    elif pm25 <= 100:
        aqi_level = 'Moderate'
        aqi_color = '#F59E0B'
    elif pm25 <= 200:
        aqi_level = 'Poor'
        aqi_color = '#EF4444'
    else:
        aqi_level = 'Severe'
        aqi_color = '#7F1D1D'
    
    return jsonify({
        'location': {
            'name': result['location']['name'],
            'region': result['location'].get('region', ''),
            'country': result['location']['country']
        },
        'aqi': {
            'value': round(pm25, 1),
            'level': aqi_level,
            'color': aqi_color
        },
        'pollutants': {
            'pm2_5': round(aqi_data.get('pm2_5', 0), 1),
            'pm10': round(aqi_data.get('pm10', 0), 1),
            'o3': round(aqi_data.get('o3', 0), 1),
            'no2': round(aqi_data.get('no2', 0), 1),
            'so2': round(aqi_data.get('so2', 0), 1),
            'co': round(aqi_data.get('co', 0), 1)
        }
    })

@app.route('/api/weather/astronomy', methods=['GET'])
@cached(timeout=3600)
def get_astronomy():
    """
    Get sunrise, sunset, and moon data for any city, state, or country
    Examples:
    - /api/weather/astronomy?city=Mumbai
    - /api/weather/astronomy?city=California
    """
    city = request.args.get('city')
    state = request.args.get('state')
    country = request.args.get('country')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    # Build query string
    if lat and lon:
        query = f"{lat},{lon}"
    elif city and state and country:
        query = f"{city},{state},{country}"
    elif city and state:
        query = f"{city},{state}"
    elif city:
        query = city
    else:
        return jsonify({'error': 'Please provide city, state, country, or coordinates'}), 400
    
    result = make_api_request('astronomy.json', {'q': query})
    
    if 'error' in result:
        return jsonify({'error': result['error']['message']}), 404
    
    return jsonify({
        'location': {
            'name': result['location']['name'],
            'region': result['location'].get('region', ''),
            'country': result['location']['country']
        },
        'astronomy': {
            'sunrise': result['astronomy']['astro']['sunrise'],
            'sunset': result['astronomy']['astro']['sunset'],
            'moonrise': result['astronomy']['astro']['moonrise'],
            'moonset': result['astronomy']['astro']['moonset'],
            'moon_phase': result['astronomy']['astro']['moon_phase'],
            'moon_illumination': result['astronomy']['astro']['moon_illumination']
        }
    })

@app.route('/api/weather/search', methods=['GET'])
@cached(timeout=600)
def search_locations():
    """
    Search for cities, states, or countries
    Examples:
    - /api/weather/search?q=Mum
    - /api/weather/search?q=New York
    - /api/weather/search?q=California
    """
    query = request.args.get('q', '')
    
    if not query or len(query) < 2:
        return jsonify({'error': 'Please provide at least 2 characters for search'}), 400
    
    result = make_api_request('search.json', {'q': query})
    
    if 'error' in result:
        return jsonify({'error': result['error']['message']}), 404
    
    locations = []
    for loc in result:
        locations.append({
            'id': loc['id'],
            'name': loc['name'],
            'region': loc.get('region', ''),
            'country': loc['country'],
            'lat': loc['lat'],
            'lon': loc['lon'],
            'url': loc['url']
        })
    
    return jsonify({
        'query': query,
        'results': locations,
        'count': len(locations)
    })

@app.route('/api/weather/alerts', methods=['GET'])
@cached(timeout=180)
def get_weather_alerts():
    """
    Get weather alerts for any city, state, or country
    Examples:
    - /api/weather/alerts?city=Mumbai
    - /api/weather/alerts?city=Florida
    """
    city = request.args.get('city')
    state = request.args.get('state')
    country = request.args.get('country')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    # Build query string
    if lat and lon:
        query = f"{lat},{lon}"
    elif city and state and country:
        query = f"{city},{state},{country}"
    elif city and state:
        query = f"{city},{state}"
    elif city:
        query = city
    else:
        return jsonify({'error': 'Please provide city, state, country, or coordinates'}), 400
    
    result = make_api_request('forecast.json', {'q': query, 'days': 1, 'alerts': 'yes'})
    
    if 'error' in result:
        return jsonify({'error': result['error']['message']}), 404
    
    alerts = result.get('alerts', {}).get('alert', [])
    
    return jsonify({
        'location': {
            'name': result['location']['name'],
            'region': result['location'].get('region', ''),
            'country': result['location']['country']
        },
        'alerts': [
            {
                'headline': alert.get('headline', 'Weather Alert'),
                'severity': alert.get('severity', 'Unknown'),
                'description': alert.get('desc', 'No description available'),
                'instruction': alert.get('instruction', ''),
                'effective': alert.get('effective', ''),
                'expires': alert.get('expires', '')
            }
            for alert in alerts
        ]
    })

@app.route('/api/weather/all', methods=['GET'])
@cached(timeout=300)
def get_all_weather():
    """
    Get complete weather data (current, forecast, air quality) for any location
    Examples:
    - /api/weather/all?city=Mumbai
    - /api/weather/all?city=California
    - /api/weather/all?city=New York
    - /api/weather/all?lat=19.0760&lon=72.8777
    """
    city = request.args.get('city')
    state = request.args.get('state')
    country = request.args.get('country')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    # Build query string
    if lat and lon:
        query = f"{lat},{lon}"
    elif city and state and country:
        query = f"{city},{state},{country}"
    elif city and state:
        query = f"{city},{state}"
    elif city:
        query = city
    else:
        return jsonify({'error': 'Please provide city, state, country, or coordinates'}), 400
    
    # Get current weather and forecast
    forecast_result = make_api_request('forecast.json', {
        'q': query, 
        'days': 5, 
        'aqi': 'yes',
        'alerts': 'yes'
    })
    
    if 'error' in forecast_result:
        return jsonify({'error': forecast_result['error']['message']}), 404
    
    # Get astronomy data
    astronomy_result = make_api_request('astronomy.json', {'q': query})
    
    # Prepare complete response
    response = {
        'location': {
            'name': forecast_result['location']['name'],
            'region': forecast_result['location'].get('region', ''),
            'country': forecast_result['location']['country'],
            'localtime': forecast_result['location']['localtime'],
            'lat': forecast_result['location']['lat'],
            'lon': forecast_result['location']['lon']
        },
        'current': {
            'temp_c': forecast_result['current']['temp_c'],
            'temp_f': forecast_result['current']['temp_f'],
            'condition': forecast_result['current']['condition']['text'],
            'condition_icon': forecast_result['current']['condition']['icon'],
            'wind_kph': forecast_result['current']['wind_kph'],
            'wind_dir': forecast_result['current']['wind_dir'],
            'humidity': forecast_result['current']['humidity'],
            'pressure_mb': forecast_result['current']['pressure_mb'],
            'feelslike_c': forecast_result['current']['feelslike_c'],
            'vis_km': forecast_result['current']['vis_km'],
            'uv': forecast_result['current']['uv'],
            'gust_kph': forecast_result['current'].get('gust_kph', 0),
            'cloud': forecast_result['current']['cloud'],
            'precip_mm': forecast_result['current']['precip_mm']
        },
        'air_quality': forecast_result['current'].get('air_quality', {}),
        'forecast': [],
        'astronomy': {
            'sunrise': astronomy_result.get('astronomy', {}).get('astro', {}).get('sunrise', 'N/A'),
            'sunset': astronomy_result.get('astronomy', {}).get('astro', {}).get('sunset', 'N/A'),
            'moon_phase': astronomy_result.get('astronomy', {}).get('astro', {}).get('moon_phase', 'N/A'),
            'moon_illumination': astronomy_result.get('astronomy', {}).get('astro', {}).get('moon_illumination', 'N/A')
        },
        'alerts': forecast_result.get('alerts', {}).get('alert', [])
    }
    
    # Add forecast data
    for day in forecast_result['forecast']['forecastday']:
        response['forecast'].append({
            'date': day['date'],
            'max_temp_c': day['day']['maxtemp_c'],
            'min_temp_c': day['day']['mintemp_c'],
            'avg_temp_c': day['day']['avgtemp_c'],
            'condition': day['day']['condition']['text'],
            'condition_icon': day['day']['condition']['icon'],
            'rain_chance': day['day']['daily_chance_of_rain'],
            'snow_chance': day['day']['daily_chance_of_snow'],
            'wind_kph': day['day']['maxwind_kph'],
            'humidity': day['day']['avghumidity'],
            'uv': day['day']['uv'],
            'sunrise': day['astro']['sunrise'],
            'sunset': day['astro']['sunset']
        })
    
    return jsonify(response)

@app.route('/api/weather/cache/clear', methods=['POST'])
def clear_cache():
    """Clear the cache (useful for debugging)"""
    global cache
    cache.clear()
    return jsonify({
        'message': 'Cache cleared successfully',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/weather/stats', methods=['GET'])
def get_stats():
    """Get API statistics"""
    return jsonify({
        'cache_size': len(cache),
        'status': 'running',
        'uptime': 'Server is active',
        'timestamp': datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🌤️ WeatherSphere Backend Server")
    print("=" * 60)
    print(f"📍 Server running on: http://localhost:5000")
    print(f"🔑 API Key configured: {'✅ Yes' if WEATHER_API_KEY else '❌ No'}")
    print(f"💾 Cache timeout: {CACHE_TIMEOUT} seconds")
    print("\n📡 Available Endpoints:")
    print("=" * 60)
    print("  GET  /health                                    - Health check")
    print("  GET  /api/weather/current?city=Mumbai           - Current weather")
    print("  GET  /api/weather/forecast?city=Mumbai&days=5   - 5-day forecast")
    print("  GET  /api/weather/hourly?city=Mumbai&hours=12   - Hourly forecast")
    print("  GET  /api/weather/air-quality?city=Mumbai       - Air quality")
    print("  GET  /api/weather/astronomy?city=Mumbai         - Sunrise/Sunset")
    print("  GET  /api/weather/search?q=Mum                  - Search locations")
    print("  GET  /api/weather/alerts?city=Mumbai            - Weather alerts")
    print("  GET  /api/weather/all?city=Mumbai               - Complete weather data")
    print("  POST /api/weather/cache/clear                   - Clear cache")
    print("  GET  /api/weather/stats                         - Server statistics")
    print("=" * 60)
    print("\n🌍 Supported queries:")
    print("  • Cities: Mumbai, New York, London, Tokyo, Paris")
    print("  • States: California, Texas, Maharashtra, Gujarat")
    print("  • Countries: India, USA, UK, Japan, France")
    print("  • With coordinates: lat=19.0760&lon=72.8777")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)