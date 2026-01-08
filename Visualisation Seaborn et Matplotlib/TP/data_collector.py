#!/usr/bin/env python3
"""
🚍 Nice Traffic Watch - Data Collector
=======================================
Elegant, resilient scraper for Lignes d'Azur GTFS-RT feeds.

This script continuously collects real-time transit data, merging vehicle positions
with trip delay information to build a comprehensive historical dataset for analysis.

Architecture:
- Fetches both trip_updates (delays) and vehicle_positions (GPS) every minute
- Merges data by trip_id to create enriched observations
- Saves to CSV with proper timestamp formatting
- Handles errors gracefully with exponential backoff
- Logs all activity for transparency

Author: Data Analyst Consultant
Date: 2026-01-08
"""

import csv
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import requests
from google.transit import gtfs_realtime_pb2


# ============================================================================
# Configuration
# ============================================================================

TRIP_UPDATES_URL = "https://ara-api.enroute.mobi/rla/gtfs/trip-updates"
VEHICLE_POSITIONS_URL = "https://ara-api.enroute.mobi/rla/gtfs/vehicle-positions"
COLLECTION_INTERVAL = 60  # seconds (1 minute)
DATA_DIR = Path("data")
CSV_FILE = DATA_DIR / "transit_observations.csv"
LOG_FILE = DATA_DIR / "collector.log"

CSV_HEADERS = [
    "timestamp",           # ISO 8601 datetime of observation
    "trip_id",            # Unique trip identifier
    "route_id",           # Bus/Tram line number (e.g., "09", "61")
    "vehicle_id",         # Vehicle identifier
    "delay_seconds",      # Delay in seconds (negative = early, positive = late)
    "latitude",           # GPS latitude
    "longitude",          # GPS longitude
]


# ============================================================================
# Logging Setup
# ============================================================================

def setup_logging():
    """Configure logging to both file and console with elegant formatting."""
    DATA_DIR.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)8s | %(message)s',
        datefmt='%H:%M:%S',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


# ============================================================================
# Data Fetching
# ============================================================================

def fetch_gtfs_rt(url: str, timeout: int = 10) -> Optional[gtfs_realtime_pb2.FeedMessage]:
    """
    Fetch and parse a GTFS-RT feed.

    Args:
        url: The GTFS-RT endpoint URL
        timeout: Request timeout in seconds

    Returns:
        Parsed FeedMessage or None if fetch fails
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        return feed
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to parse feed from {url}: {e}")
        return None


def extract_trip_delays(feed: gtfs_realtime_pb2.FeedMessage) -> Dict[str, int]:
    """
    Extract delay information from trip updates feed.

    Returns:
        Dictionary mapping trip_id to average delay in seconds
    """
    delays = {}

    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            continue

        trip_update = entity.trip_update
        trip_id = trip_update.trip.trip_id

        # Calculate average delay across all stop time updates
        stop_delays = []
        for stu in trip_update.stop_time_update:
            if stu.HasField("arrival") and stu.arrival.HasField("delay"):
                stop_delays.append(stu.arrival.delay)
            elif stu.HasField("departure") and stu.departure.HasField("delay"):
                stop_delays.append(stu.departure.delay)

        if stop_delays:
            delays[trip_id] = int(sum(stop_delays) / len(stop_delays))

    return delays


def extract_vehicle_positions(feed: gtfs_realtime_pb2.FeedMessage) -> List[Dict]:
    """
    Extract vehicle position information.

    Returns:
        List of dictionaries with vehicle data
    """
    vehicles = []

    for entity in feed.entity:
        if not entity.HasField("vehicle"):
            continue

        vehicle = entity.vehicle

        # Skip vehicles without position or trip info
        if not vehicle.HasField("position") or not vehicle.trip.trip_id:
            continue

        vehicles.append({
            "trip_id": vehicle.trip.trip_id,
            "route_id": vehicle.trip.route_id,
            "vehicle_id": vehicle.vehicle.id if vehicle.HasField("vehicle") else "",
            "latitude": vehicle.position.latitude,
            "longitude": vehicle.position.longitude,
        })

    return vehicles


# ============================================================================
# Data Collection & Storage
# ============================================================================

def collect_observations() -> List[Dict]:
    """
    Collect one round of observations by fetching and merging both feeds.

    Returns:
        List of observation dictionaries ready for CSV writing
    """
    logger.info("🔄 Fetching GTFS-RT feeds...")

    # Fetch both feeds
    trip_feed = fetch_gtfs_rt(TRIP_UPDATES_URL)
    vehicle_feed = fetch_gtfs_rt(VEHICLE_POSITIONS_URL)

    if not trip_feed or not vehicle_feed:
        logger.warning("⚠️  Failed to fetch one or both feeds, skipping this round")
        return []

    # Extract data
    delays = extract_trip_delays(trip_feed)
    vehicles = extract_vehicle_positions(vehicle_feed)

    logger.info(f"📊 Found {len(delays)} trips with delay info, {len(vehicles)} vehicles with positions")

    # Merge: add delay information to each vehicle observation
    timestamp = datetime.now().isoformat()
    observations = []

    for vehicle in vehicles:
        trip_id = vehicle["trip_id"]
        delay = delays.get(trip_id, 0)  # Default to 0 if no delay info

        observations.append({
            "timestamp": timestamp,
            "trip_id": trip_id,
            "route_id": vehicle["route_id"],
            "vehicle_id": vehicle["vehicle_id"],
            "delay_seconds": delay,
            "latitude": vehicle["latitude"],
            "longitude": vehicle["longitude"],
        })

    logger.info(f"✅ Collected {len(observations)} enriched observations")
    return observations


def save_observations(observations: List[Dict]):
    """
    Append observations to CSV file (creates file with headers if needed).
    """
    if not observations:
        return

    # Create data directory if needed
    DATA_DIR.mkdir(exist_ok=True)

    # Check if file exists to determine if we need to write headers
    file_exists = CSV_FILE.exists()

    try:
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)

            if not file_exists:
                writer.writeheader()
                logger.info(f"📝 Created new CSV file: {CSV_FILE}")

            writer.writerows(observations)
            logger.info(f"💾 Saved {len(observations)} observations to {CSV_FILE}")

    except Exception as e:
        logger.error(f"❌ Failed to save observations: {e}")


# ============================================================================
# Main Collection Loop
# ============================================================================

def run_collector(duration_hours: Optional[float] = None):
    """
    Run the data collector continuously.

    Args:
        duration_hours: If specified, run for this many hours then stop.
                       If None, run indefinitely.
    """
    logger.info("=" * 70)
    logger.info("🚍 Nice Traffic Watch - Data Collector Started")
    logger.info("=" * 70)
    logger.info(f"📂 Data directory: {DATA_DIR.absolute()}")
    logger.info(f"📄 CSV file: {CSV_FILE.absolute()}")
    logger.info(f"⏱️  Collection interval: {COLLECTION_INTERVAL} seconds")

    if duration_hours:
        logger.info(f"⏲️  Will run for {duration_hours} hours")
        end_time = time.time() + (duration_hours * 3600)
    else:
        logger.info("♾️  Running indefinitely (Ctrl+C to stop)")
        end_time = None

    logger.info("=" * 70)

    collection_count = 0
    error_count = 0

    try:
        while True:
            # Check if we should stop
            if end_time and time.time() >= end_time:
                logger.info("⏰ Time limit reached, stopping collector")
                break

            collection_start = time.time()

            # Collect and save data
            try:
                observations = collect_observations()
                save_observations(observations)
                collection_count += 1
                error_count = 0  # Reset error count on success
            except Exception as e:
                error_count += 1
                logger.error(f"❌ Collection failed: {e}")

                # If too many consecutive errors, wait longer
                if error_count >= 3:
                    backoff = min(300, COLLECTION_INTERVAL * error_count)
                    logger.warning(f"⚠️  {error_count} consecutive errors, backing off {backoff}s")
                    time.sleep(backoff)
                    continue

            # Calculate how long to sleep
            elapsed = time.time() - collection_start
            sleep_time = max(0, COLLECTION_INTERVAL - elapsed)

            if sleep_time > 0:
                logger.info(f"💤 Next collection in {sleep_time:.1f}s (Total collections: {collection_count})")
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        logger.info("\n" + "=" * 70)
        logger.info("⛔ Collector stopped by user (Ctrl+C)")

    finally:
        logger.info("=" * 70)
        logger.info(f"📊 Final Stats:")
        logger.info(f"   - Total collections: {collection_count}")
        logger.info(f"   - CSV file: {CSV_FILE.absolute()}")
        if CSV_FILE.exists():
            size_mb = CSV_FILE.stat().st_size / 1024 / 1024
            logger.info(f"   - File size: {size_mb:.2f} MB")
        logger.info("=" * 70)
        logger.info("👋 Goodbye!")


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    logger = setup_logging()

    # Run for 8 hours (full work day) or indefinitely if you want
    # For testing, you can set a shorter duration like 0.1 hours (6 minutes)
    run_collector(duration_hours=None)  # Run indefinitely
