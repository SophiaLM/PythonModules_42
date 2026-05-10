from datetime import datetime

from pydantic import BaseModel, Field


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")

    valid_station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2024, 1, 15, 10, 30),
        is_operational=True,
    )

    print("Valid station created:")
    print(f"  ID: {valid_station.station_id}")
    print(f"  Name: {valid_station.name}")
    print(f"  Crew: {valid_station.crew_size} people")
    print(f"  Power: {valid_station.power_level}%")
    print(f"  Oxygen: {valid_station.oxygen_level}%")
    is_op = valid_station.is_operational
    status = "Operational" if is_op else "Non-operational"
    print(f"  Status: {status}")

    print("========================================")
    print("Expected validation error:")

    try:
        SpaceStation(
            station_id="ISS002",
            name="Test Station",
            crew_size=25,
            power_level=80.0,
            oxygen_level=90.0,
            last_maintenance=datetime.now(),
        )
    except Exception as e:
        print(f"  {e}")


if __name__ == "__main__":
    main()
