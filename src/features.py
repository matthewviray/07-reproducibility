import pandas as pd
from pathlib import Path

INPUT = Path("data/transformed/events.csv")
OUTPUT = Path("data/features/events.csv")


def main():
    df = pd.read_csv(INPUT)

    df["duration_minutes"] = df["duration_seconds"] / 60
    df["weekday"] = pd.to_datetime(df["date"]).dt.strftime("%A")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)
    print(f"features: {len(df)} rows written to {OUTPUT}")


if __name__ == "__main__":
    main()