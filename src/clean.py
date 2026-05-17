import pandas as pd
from pathlib import Path

VALID_EVENT_TYPES = {"click", "scroll", "view", "login", "purchase"}

INPUT = Path("data/raw/events.csv")
OUTPUT = Path("data/clean/events.csv")


def parse_timestamp(ts):
    """Try multiple formats; return a normalized datetime or NaT."""
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f",  # 2026-04-28T00:51:56.561
        "%Y-%m-%dT%H:%M:%S",     # 2026-04-28T00:51:56
        "%Y-%m-%d %H:%M:%S",     # 2026-02-28 10:29:30
        "%m/%d/%Y %H:%M:%S",     # 01/25/2026 06:45:26
    ]
    for fmt in formats:
        try:
            return pd.to_datetime(ts, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT


def main():
    df = pd.read_csv(INPUT, dtype=str)

    # Drop rows with any missing fields
    df = df.dropna(subset=["user_id", "timestamp", "event_type", "duration_seconds"])
    df = df[df["user_id"].str.strip() != ""]
    df = df[df["timestamp"].str.strip() != ""]
    df = df[df["event_type"].str.strip() != ""]
    df = df[df["duration_seconds"].str.strip() != ""]

    # Drop invalid event_type (must match exactly, case-sensitive)
    df = df[df["event_type"].isin(VALID_EVENT_TYPES)]

    # Convert duration_seconds to numeric and drop non-positive
    df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")
    df = df.dropna(subset=["duration_seconds"])
    df = df[df["duration_seconds"] > 0]

    # Normalize timestamps to ISO 8601 (YYYY-MM-DDTHH:MM:SS)
    df["timestamp"] = df["timestamp"].apply(parse_timestamp)
    df = df.dropna(subset=["timestamp"])
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

    # Convert duration back to int
    df["duration_seconds"] = df["duration_seconds"].astype(int)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)
    print(f"clean: {len(df)} rows written to {OUTPUT}")


if __name__ == "__main__":
    main()