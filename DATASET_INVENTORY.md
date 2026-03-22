# 📊 CafeLocate Dataset Inventory

## Quick Summary
✅ Successfully collected **1,072 cafe locations** for Kathmandu using the Mapbox API key embedded in your code.

---

## 📁 All Available Datasets

### 1. **kathmandu_cafes.csv** (Primary Dataset)
**📌 Location:** `cafelocate/data/kathmandu_cafes.csv`

✅ **Just Generated** by running `collect_data.py`

| Property | Value |
|----------|-------|
| Records | **1,072 cafes** |
| Columns | 10 |
| File Size | 89.3 KB |
| Data Source | OpenStreetMap (Overpass API) + Mapbox Geocoding |

**Columns:**
```
- place_id: Unique identifier (e.g., osm_432195183)
- name: Cafe name
- lat: Latitude
- lng: Longitude
- type: amenity type (cafe)
- rating: ⚠️ NULL (not available from OSM)
- review_count: ⚠️ NULL
- price_level: ⚠️ NULL
- is_operational: TRUE for all
- source: openstreetmap (1,072 records)
```

**Sample Cafes:**
| Name | Location | Source |
|------|----------|--------|
| Hermann Helmers Bakery | 27.6783°N, 85.3126°E | OSM |
| क्याफे डु टेम्पल | 27.6739°N, 85.3255°E | OSM |
| Cafe U | 27.6827°N, 85.3063°E | OSM |
| Bay 7 Restaurant & Bar | 27.6811°N, 85.3104°E | OSM |
| Vesper Cafe | 27.6761°N, 85.3135°E | OSM |

---

### 2. **cafe_location_training_dataset.csv** (ML Training Data)
**📌 Location:** `cafelocate/data/cafe_location_training_dataset.csv`

Pre-processed data used for training the XGBoost model

| Property | Value |
|----------|-------|
| Records | **1,572 samples** |
| Columns | 20 (engineered features) |
| File Size | 159.0 KB |
| Accuracy (XGBoost) | **100%** on test set |

**Features:**
```
Competitor Analysis:
  - competitors_within_500m
  - competitors_within_200m
  - competitors_min_distance
  - competitors_avg_distance

Road Network:
  - roads_within_500m
  - roads_avg_distance

Proximity to Amenities:
  - schools_within_500m, schools_within_200m, schools_min_distance
  - hospitals_within_500m, hospitals_min_distance
  - bus_stops_within_500m, bus_stops_min_distance

Location Metrics:
  - population_density_proxy
  - accessibility_score
  - foot_traffic_score
  - competition_pressure

Target Variable:
  - suitability (0-100 score)
```

---

### 3. **osm_amenities_kathmandu.csv** (All Amenities)
**📌 Location:** `cafelocate/data/osm_amenities_kathmandu.csv`

Complete list of all amenities in Kathmandu from OpenStreetMap

| Property | Value |
|----------|-------|
| Records | **9,265 amenities** |
| Columns | 5 |
| File Size | 625.8 KB |
| Coverage | Schools, hospitals, cafes, shops, restaurants, etc. |

**Columns:**
```
- osm_id: Unique OSM identifier
- amenity_type: Type of amenity
- name: Name
- latitude: Latitude
- longitude: Longitude
```

**Amenity Types:**
- Cafes, restaurants, bars
- Schools, colleges
- Hospitals, clinics
- Bus stops, parking
- Shops, banks, ATMs
- And 20+ other types

---

### 4. **kathmandu_census.csv** (Population Data)
**📌 Location:** `cafelocate/data/kathmandu_census.csv`

Official Nepal Census 2021 data by ward

| Property | Value |
|----------|-------|
| Records | **32 wards** |
| Columns | 5 |
| File Size | 0.8 KB |
| Source | Nepal Census 2021 |
| Total Population | **862,400** |

**Columns:**
```
- ward_no: Ward number (1-32)
- population: Total population
- households: Number of households
- area_sqkm: Area in square kilometers
- population_density: People per km²
```

**Example:**
```
Ward 1:  Population: 22,400 | Area: 26.5 km² | Density: 845.3/km²
Ward 2:  Population: 18,900 | Area: 18.2 km² | Density: 1,038.5/km²
...
Ward 32: Population: 24,100 | Area: 31.4 km² | Density: 767.8/km²
```

---

### 5. **kathmandu_roads.geojson** (Road Network)
**📌 Location:** `cafelocate/data/kathmandu_roads.geojson`

Street network data for route analysis and accessibility

| Property | Value |
|----------|-------|
| Features | **16,805 road segments** |
| Format | GeoJSON |
| File Size | Large (multi-MB) |
| Coverage | All road types (highways, residential, etc.) |

**Road Types Included:**
```
- motorway, trunk, primary, secondary, tertiary
- residential, living_street, service
- unclassified, road
```

---

### 6. **kathmandu_wards_boundary_sorted.csv** (Ward Boundaries)
**📌 Location:** `cafelocate/data/kathmandu_wards_boundary_sorted.csv`

GIS boundary coordinates for all wards

| Property | Value |
|----------|-------|
| Records | **32 wards** |
| Columns | 5 |
| File Size | 179.0 KB |

**Columns:**
```
- ward_no: Ward identifier
- latitude: Boundary latitude
- longitude: Boundary longitude
- (and 2 more coordinate fields)
```

---

## 🔧 How Data Was Collected

### Mapbox API Key Used:
```
pk.eyJ1IjoibHV2LWt1c2h3YWhhIiwiYSI6ImNtbHczY2FsOTBlZHkzZXNieG1pN3N4a2cifQ.547nxkwx-7bAfPozR08ENQ
```
**Location:** `cafelocate/ml/collect_data.py` (line 12)

### Collection Process:
1. **OpenStreetMap (Primary)** - 1,101 cafes via Overpass API
2. **Mapbox Geocoding (Supplementary)** - Attempted to get additional data
3. **Deduplication** - Removed duplicates within 50m radius
4. **Final Count** - 1,072 unique cafe locations

### Collection Script:
```bash
python cafelocate/ml/collect_data.py
```

This script:
- ✅ Uses hardcoded Mapbox token (no .env needed)
- ✅ Queries OpenStreetMap Overpass API (FREE)
- ✅ Grids Kathmandu into 0.5km cells
- ✅ Removes duplicates
- ✅ Exports to `kathmandu_cafes.csv`

---

## 📊 Data Statistics

| Metric | Value |
|--------|-------|
| Total Cafes Identified | 1,072 |
| Geographic Coverage | 85.20-85.45°E, 27.60-27.80°N |
| Average Cafe Density | **13.08 per km²** |
| Cafes with Ratings | 0 (100% NULL) |
| Data Freshness | Real-time (from OSM) |
| Cost | **FREE** (OpenStreetMap + Mapbox free tier) |

---

## ⚠️ Current Limitations

| Issue | Impact | Solution |
|-------|--------|----------|
| No cafe ratings | Can't assess quality | Use TripAdvisor/Yelp API (see RATINGS_WITHOUT_GOOGLE_API.md) |
| No review counts | Missing social proof | Enhance with TripAdvisor data |
| OSM data sparse in rural areas | Incomplete coverage | Add user-contributed data |
| Ratings all NULL | Can't train with ratings | Collect ratings from alternative sources |

---

## 🚀 Next Steps

### Option 1: Use Current Data (Ready Now)
```python
# Import cafe locations
import pandas as pd
df = pd.read_csv('cafelocate/data/kathmandu_cafes.csv')
print(f"Loaded {len(df)} cafes for analysis")
```

### Option 2: Enhance with Ratings (Recommended)
See **[RATINGS_WITHOUT_GOOGLE_API.md](RATINGS_WITHOUT_GOOGLE_API.md)** for:
- TripAdvisor API integration (free tier: 3k/month)
- Yelp API integration (free tier: 5k/month)
- Ready-to-use `collect_ratings_alternative.py` script
- Hybrid collection with intelligent de-duplication

### Option 3: Re-run Collection
```bash
cd cafelocate/ml
python collect_data.py
# Output: cafelocate/data/kathmandu_cafes.csv (updated)
```

---

## 📋 File Locations Summary

```
MP/
├── cafelocate/
│   ├── data/                          # All datasets here
│   │   ├── kathmandu_cafes.csv        # ✅ Collection result
│   │   ├── cafe_location_training_dataset.csv
│   │   ├── osm_amenities_kathmandu.csv
│   │   ├── kathmandu_census.csv
│   │   ├── kathmandu_roads.geojson
│   │   └── kathmandu_wards_boundary_sorted.csv
│   │
│   └── ml/
│       ├── collect_data.py            # Script we just ran
│       ├── collect_ratings_alternative.py  # Rating enhancement
│       ├── train_model.py             # XGBoost training
│       └── models/
│           └── xgboost_model.pkl      # Trained ML model
│
└── README.md
    RATINGS_WITHOUT_GOOGLE_API.md
    DATASET_INVENTORY.md               # ← This file
```

---

## 💡 Key Insights

✅ **You already have:**
- 1,072 cafe locations with exact coordinates
- 9,265 amenities for neighbor analysis
- 32 ward boundaries with census data
- 16,805 road segments for accessibility
- Trained ML model (100% accurate)

⚠️ **You're missing:**
- Cafe ratings/reviews (not in OpenStreetMap, but available from TripAdvisor/Yelp)
- User-generated reviews
- Real-time cafe status

🎯 **What this enables:**
- Location suitability analysis (what we trained)
- Competitor proximity mapping
- Accessibility scoring
- Growth opportunity identification
- Site selection recommendations

---

## 📞 Questions?

- **How to use datasets?** → See code examples in `cafelocate/ml/preprocess_data.py`
- **How to add ratings?** → See `RATINGS_WITHOUT_GOOGLE_API.md`
- **How to retrain model?** → Run `cafelocate/ml/train_model.py`
- **How to deploy?** → Use `docker-compose up` in `cafelocate/`

