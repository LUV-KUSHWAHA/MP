"""
CafeLocate ML - Data Collection Script
Scrapes café data from Mapbox Geocoding API and OpenStreetMap
"""

import requests
import pandas as pd
import time
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Mapbox configuration
MAPBOX_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN')
if not MAPBOX_TOKEN or MAPBOX_TOKEN == 'your_mapbox_access_token_here':
    print("Warning: MAPBOX_ACCESS_TOKEN not set. Skipping Mapbox data collection.")
    MAPBOX_TOKEN = None

# Kathmandu bounding box (approximate)
KATHMANDU_BBOX = {
    'min_lng': 85.2,
    'max_lng': 85.4,
    'min_lat': 27.65,
    'max_lat': 27.75
}

def create_grid_points(bbox, grid_size_km=1.0):
    """
    Create a grid of points across Kathmandu for API calls
    grid_size_km: distance between grid points in kilometers
    """
    import math

    # Convert km to approximate degrees (rough approximation)
    km_to_deg = grid_size_km / 111.0  # 1 degree ≈ 111 km

    points = []
    lat = bbox['min_lat']
    while lat <= bbox['max_lat']:
        lng = bbox['min_lng']
        while lng <= bbox['max_lng']:
            points.append((lng, lat))
            lng += km_to_deg
        lat += km_to_deg

    return points

def search_cafes_mapbox(lng, lat, radius=1000):
    """
    Search for cafes using Mapbox Geocoding API
    """
    url = "https://api.mapbox.com/geocoding/v5/mapbox.places/cafe.json"

    params = {
        'access_token': MAPBOX_TOKEN,
        'proximity': f"{lng},{lat}",
        'limit': 10,
        'types': 'poi',
        'bbox': [
            lng - 0.01, lat - 0.01,  # Small bbox around search point
            lng + 0.01, lat + 0.01
        ]
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error searching cafes at {lng},{lat}: {e}")
        return None

def get_osm_cafes():
    """
    Get café data from OpenStreetMap using Overpass API
    This provides more comprehensive local data
    """
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Simpler query for cafes in Kathmandu bounding box
    # Using bbox instead of area to avoid timeout
    query = """
    [out:json][timeout:30];
    (
      node["amenity"="cafe"](27.65,85.2,27.75,85.4);
      way["amenity"="cafe"](27.65,85.2,27.75,85.4);
    );
    out center;
    """

    try:
        response = requests.post(overpass_url, data={'data': query}, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching OSM data: {e}")
        return None

def parse_osm_cafes(osm_data):
    """
    Parse OpenStreetMap café data into standardized format
    """
    cafes = []

    if not osm_data or 'elements' not in osm_data:
        return cafes

    for element in osm_data['elements']:
        if element.get('type') == 'node':
            lat = element.get('lat')
            lng = element.get('lon')
        elif 'center' in element:
            center = element['center']
            lat = center.get('lat')
            lng = center.get('lon')  # Try 'lon' instead of 'lng'
            if lng is None:
                lng = center.get('lng')  # Fallback to 'lng'
        else:
            continue

        if lat is None or lng is None:
            continue

        cafe = {
            'place_id': f"osm_{element['id']}",
            'name': element.get('tags', {}).get('name', 'Unknown Cafe'),
            'lat': lat,
            'lng': lng,
            'type': 'cafe',
            'rating': None,  # OSM doesn't have ratings
            'review_count': None,
            'price_level': None,
            'is_operational': True,
            'source': 'openstreetmap'
        }
        cafes.append(cafe)

    return cafes

def collect_cafe_data():
    """
    Main function to collect café data from multiple sources
    """
    print("Starting café data collection...")

    all_cafes = []

    # 1. Get data from OpenStreetMap (primary source)
    print("Fetching café data from OpenStreetMap...")
    osm_data = get_osm_cafes()
    print(f"OSM data received: {osm_data is not None}")
    if osm_data:
        osm_cafes = parse_osm_cafes(osm_data)
        all_cafes.extend(osm_cafes)
        print(f"Found {len(osm_cafes)} cafes from OpenStreetMap")
        print(f"Sample cafe: {osm_cafes[0] if osm_cafes else 'None'}")
    else:
        print("No OSM data received")

    # 2. Supplement with Mapbox Geocoding (for additional coverage)
    if MAPBOX_TOKEN:
        print("Supplementing with Mapbox Geocoding API...")
        grid_points = create_grid_points(KATHMANDU_BBOX, grid_size_km=0.5)

        mapbox_cafes = []
        for i, (lng, lat) in enumerate(grid_points):
            if i % 10 == 0:
                print(f"Processed {i}/{len(grid_points)} grid points...")

            result = search_cafes_mapbox(lng, lat)
            if result and 'features' in result:
                for feature in result['features']:
                    if feature['place_type'] == ['poi']:
                        properties = feature['properties']
                        geometry = feature['geometry']

                        cafe = {
                            'place_id': f"mapbox_{feature['id']}",
                            'name': properties.get('name', 'Unknown Cafe'),
                            'lat': geometry['coordinates'][1],
                            'lng': geometry['coordinates'][0],
                            'type': 'cafe',
                            'rating': None,
                            'review_count': None,
                            'price_level': None,
                            'is_operational': True,
                            'source': 'mapbox'
                        }
                        mapbox_cafes.append(cafe)

            # Rate limiting
            time.sleep(0.1)

        print(f"Found {len(mapbox_cafes)} additional cafes from Mapbox")
        all_cafes.extend(mapbox_cafes)
    else:
        print("Skipping Mapbox data collection (no valid token)")

    # Remove duplicates based on coordinates (within 50m)
    print("Removing duplicates...")
    if not all_cafes:
        print("No café data collected from any source")
        df_deduped = pd.DataFrame()
    else:
        df = pd.DataFrame(all_cafes)

        # Simple deduplication based on rounded coordinates
        df['lat_round'] = df['lat'].round(4)  # ~11m precision
        df['lng_round'] = df['lng'].round(4)
        df_deduped = df.drop_duplicates(subset=['lat_round', 'lng_round'])
        df_deduped = df_deduped.drop(columns=['lat_round', 'lng_round'])

    print(f"After deduplication: {len(df_deduped)} unique cafes")

    # Save to CSV
    output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'kathmandu_cafes.csv')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    if df_deduped.empty:
        # Create empty CSV with proper headers
        df_deduped = pd.DataFrame(columns=['place_id', 'name', 'lat', 'lng', 'type', 'rating', 'review_count', 'price_level', 'is_operational', 'source'])
        print("Created empty cafes CSV with proper headers")
    else:
        print(f"Saved {len(df_deduped)} cafes to {output_file}")

    df_deduped.to_csv(output_file, index=False)

    return df_deduped

if __name__ == "__main__":
    collect_cafe_data()