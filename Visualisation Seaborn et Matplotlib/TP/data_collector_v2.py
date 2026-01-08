#!/usr/bin/env python3
"""
🚍 Nice Traffic Watch - Smart Data Collector V2
================================================
Elegant collector that calculates real delays by comparing
real-time arrivals with scheduled times from static GTFS.

This version:
- Loads static GTFS schedules into memory for fast lookups
- Calculates actual delays (not just positions)
- Enriches data with route type (bus vs tram)
- Handles missing data gracefully

Author: Data Analyst Consultant
Date: 2026-01-08
"""

import csv
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import requests
from google.transit import gtfs_realtime_pb2


# ============================================================================
# Configuration
# ============================================================================

TRIP_UPDATES_URL = "https://ara-api.enroute.mobi/rla/gtfs/trip-updates"
VEHICLE_POSITIONS_URL = "https://ara-api.enroute.mobi/rla/gtfs/vehicle-positions"
COLLECTION_INTERVAL = 60  # seconds
DATA_DIR = Path("data")
GTFS_DIR = DATA_DIR / "gtfs"
CSV_FILE = DATA_DIR / "transit_delays.csv"
LOG_FILE = DATA_DIR / "collector_v2.log"

CSV_HEADERS = [
    "timestamp",          # ISO 8601 datetime of observation
    "trip_id",            # Unique trip identifier
    "route_id",           # Line number (e.g., "09", "61")
    "route_type",         # 0=Tram, 3=Bus (GTFS standard)
    "vehicle_id",         # Vehicle identifier
    "stop_id",            # Stop where measurement was taken
    "scheduled_time",     # Scheduled arrival timestamp
    "actual_time",        # Actual arrival timestamp
    "delay_seconds",      # Delay in seconds (negative = early)
    "latitude",           # Vehicle GPS latitude
    "longitude",          # Vehicle GPS longitude
]


# ============================================================================
# GTFS Schedule Loader
# ============================================================================

class GTFSSchedule:
    """Efficient in-memory GTFS schedule for delay calculation."""

    def __init__(self, gtfs_dir: Path):
        self.gtfs_dir = gtfs_dir
        self.routes = {}  # route_id -> route_info
        self.trips = {}   # trip_id -> trip_info
        self.stop_times = defaultdict(list)  # trip_id -> [(stop_sequence, stop_id, arrival_time), ...]

    def load(self):
        """Load GTFS tables into memory."""
        logger.info("📚 Loading static GTFS schedules...")

        # Load routes (to get route_type: bus vs tram)
        routes_file = self.gtfs_dir / "routes.txt"
        with open(routes_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.routes[row['route_id']] = {
                    'route_short_name': row.get('route_short_name', row['route_id']),
                    'route_type': int(row['route_type']),
                }
        logger.info(f"   ✓ Loaded {len(self.routes)} routes")

        # Load trips (to map trip_id -> route_id)
        trips_file = self.gtfs_dir / "trips.txt"
        with open(trips_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.trips[row['trip_id']] = {
                    'route_id': row['route_id'],
                    'service_id': row.get('service_id', ''),
                }
        logger.info(f"   ✓ Loaded {len(self.trips)} trips")

        # Load stop_times (scheduled arrivals)
        # NOTE: This is a large file (36MB), we'll only keep what we need
        stop_times_file = self.gtfs_dir / "stop_times.txt"
        logger.info("   ⏳ Loading stop times (this may take a moment)...")
        with open(stop_times_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                trip_id = row['trip_id']
                stop_seq = int(row.get('stop_sequence', 0))
                stop_id = row['stop_id']
                arrival_time = row.get('arrival_time', '')

                self.stop_times[trip_id].append((stop_seq, stop_id, arrival_time))

        # Sort stop times by sequence for each trip
        for trip_id in self.stop_times:
            self.stop_times[trip_id].sort(key=lambda x: x[0])

        logger.info(f"   ✓ Loaded stop times for {len(self.stop_times)} trips")
        logger.info("✅ GTFS schedules loaded successfully!")

    def get_route_type(self, route_id: str) -> int:
        """Get route type (0=Tram, 3=Bus)."""
        return self.routes.get(route_id, {}).get('route_type', 3)

    def get_scheduled_arrival(self, trip_id: str, stop_id: str) -> Optional[str]:
        """Get scheduled arrival time for a trip at a specific stop."""
        if trip_id not in self.stop_times:
            return None

        for seq, sid, arrival_time in self.stop_times[trip_id]:
            if sid == stop_id:
                return arrival_time

        return None

    def time_to_seconds(self, time_str: str) -> int:
        """Convert HH:MM:SS to seconds since midnight (handles >24h)."""
        try:
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        except:
            return 0


# ============================================================================
# Logging Setup
# ============================================================================

def setup_logging():
    """Configure logging."""
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
    """Fetch and parse GTFS-RT feed."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        return feed
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None


def calculate_delays(trip_feed, vehicle_feed, schedule: GTFSSchedule) -> List[Dict]:
    """
    Calculate delays by comparing real-time arrivals with schedules.

    Returns:
        List of delay observations with full context
    """
    if not trip_feed or not vehicle_feed:
        return []

    # Build vehicle position lookup: trip_id -> vehicle_data
    vehicles = {}
    for entity in vehicle_feed.entity:
        if entity.HasField("vehicle"):
            v = entity.vehicle
            if v.trip.trip_id and v.HasField("position"):
                vehicles[v.trip.trip_id] = {
                    'vehicle_id': v.vehicle.id if v.HasField("vehicle") else "",
                    'latitude': v.position.latitude,
                    'longitude': v.position.longitude,
                }

    # Process trip updates to find delays
    observations = []
    timestamp = datetime.now().isoformat()

    for entity in trip_feed.entity:
        if not entity.HasField("trip_update"):
            continue

        trip_update = entity.trip_update
        trip_id = trip_update.trip.trip_id
        route_id = trip_update.trip.route_id

        # Get vehicle position if available
        vehicle_data = vehicles.get(trip_id, {})
        if not vehicle_data:
            continue  # Skip trips without vehicle position

        # Get route type from schedule
        route_type = schedule.get_route_type(route_id)

        # Process each stop time update
        for stu in trip_update.stop_time_update:
            stop_id = stu.stop_id

            # Get actual time (prefer arrival, fallback to departure)
            actual_time = None
            if stu.HasField('arrival') and stu.arrival.HasField('time'):
                actual_time = stu.arrival.time
            elif stu.HasField('departure') and stu.departure.HasField('time'):
                actual_time = stu.departure.time

            if not actual_time:
                continue

            # Get scheduled time from static GTFS
            scheduled_time_str = schedule.get_scheduled_arrival(trip_id, stop_id)
            if not scheduled_time_str:
                continue

            # Calculate delay
            try:
                # Convert scheduled time to timestamp (approximate - assumes today)
                scheduled_seconds = schedule.time_to_seconds(scheduled_time_str)
                now = datetime.now()
                scheduled_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
                scheduled_dt += timedelta(seconds=scheduled_seconds)
                scheduled_timestamp = int(scheduled_dt.timestamp())

                # Calculate delay in seconds
                delay_seconds = actual_time - scheduled_timestamp

                # Only keep reasonable delays (-600s to +3600s)
                if -600 <= delay_seconds <= 3600:
                    observations.append({
                        'timestamp': timestamp,
                        'trip_id': trip_id,
                        'route_id': route_id,
                        'route_type': route_type,
                        'vehicle_id': vehicle_data.get('vehicle_id', ''),
                        'stop_id': stop_id,
                        'scheduled_time': scheduled_timestamp,
                        'actual_time': actual_time,
                        'delay_seconds': delay_seconds,
                        'latitude': vehicle_data.get('latitude', 0.0),
                        'longitude': vehicle_data.get('longitude', 0.0),
                    })

            except Exception as e:
                logger.debug(f"Error calculating delay for trip {trip_id}: {e}")
                continue

    return observations


# ============================================================================
# Data Collection & Storage
# ============================================================================

def collect_observations(schedule: GTFSSchedule) -> List[Dict]:
    """Collect one round of delay observations."""
    logger.info("🔄 Fetching GTFS-RT feeds...")

    trip_feed = fetch_gtfs_rt(TRIP_UPDATES_URL)
    vehicle_feed = fetch_gtfs_rt(VEHICLE_POSITIONS_URL)

    observations = calculate_delays(trip_feed, vehicle_feed, schedule)
    logger.info(f"✅ Calculated {len(observations)} delay observations")

    return observations


def save_observations(observations: List[Dict]):
    """Append observations to CSV."""
    if not observations:
        return

    file_exists = CSV_FILE.exists()

    try:
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)

            if not file_exists:
                writer.writeheader()
                logger.info(f"📝 Created new CSV: {CSV_FILE}")

            writer.writerows(observations)
            logger.info(f"💾 Saved {len(observations)} observations")

    except Exception as e:
        logger.error(f"❌ Failed to save: {e}")


# ============================================================================
# Main Loop
# ============================================================================

def run_collector(duration_hours: Optional[float] = None):
    """Run the collector."""
    logger.info("=" * 70)
    logger.info("🚍 Nice Traffic Watch - Smart Collector V2")
    logger.info("=" * 70)

    # Load GTFS schedules
    schedule = GTFSSchedule(GTFS_DIR)
    schedule.load()

    logger.info(f"📂 Data directory: {DATA_DIR.absolute()}")
    logger.info(f"📄 CSV file: {CSV_FILE.absolute()}")
    logger.info(f"⏱️  Interval: {COLLECTION_INTERVAL}s")

    if duration_hours:
        logger.info(f"⏲️  Duration: {duration_hours}h")
        end_time = time.time() + (duration_hours * 3600)
    else:
        logger.info("♾️  Running indefinitely (Ctrl+C to stop)")
        end_time = None

    logger.info("=" * 70)

    collection_count = 0
    error_count = 0

    try:
        while True:
            if end_time and time.time() >= end_time:
                break

            start = time.time()

            try:
                observations = collect_observations(schedule)
                save_observations(observations)
                collection_count += 1
                error_count = 0
            except Exception as e:
                error_count += 1
                logger.error(f"❌ Collection failed: {e}")
                if error_count >= 3:
                    backoff = min(300, COLLECTION_INTERVAL * error_count)
                    logger.warning(f"⚠️  Backing off {backoff}s")
                    time.sleep(backoff)
                    continue

            elapsed = time.time() - start
            sleep_time = max(0, COLLECTION_INTERVAL - elapsed)

            if sleep_time > 0:
                logger.info(f"💤 Next collection in {sleep_time:.1f}s (Total: {collection_count})")
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        logger.info("\n⛔ Stopped by user")

    finally:
        logger.info("=" * 70)
        logger.info(f"📊 Total collections: {collection_count}")
        if CSV_FILE.exists():
            size_mb = CSV_FILE.stat().st_size / 1024 / 1024
            logger.info(f"📦 File size: {size_mb:.2f} MB")
        logger.info("=" * 70)


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    logger = setup_logging()
    run_collector(duration_hours=None)
