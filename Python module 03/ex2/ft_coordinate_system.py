#!/usr/bin/env python3
import math


def validate_coor(coordinates: str) -> tuple:
    """
    Check that the coordinates string is valid and return a tuple.
    """
    x, y, z = coordinates.split(",")
    return (int(x), int(y), int(z))


def distance_3d(origin: tuple, position: tuple) -> float:
    """
    Calculate the 3D distance between two points using math.sqrt
    """
    x1, y1, z1 = origin
    x2, y2, z2 = position
    result = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    return (result)


def main(coord: str, origin: tuple) -> None:
    """
    Main function to parse coordinates, calculate distances, and handle errors.
    coord  → string with 'x,y,z' format
    origin → tuple with starting (x, y, z) position
    """
    try:
        print(f"Parsing coordinates: '{coord}'")
        position = validate_coor(coord)
    except ValueError as e:
        print(f"Parcing invalid coordinates: '{coord}'")
        print("Error parcing coordinates:", e)
        print(f"Error details - Type: {type(e).__name__}, arg: {e.args}")
        return None

    print(f"Parced position: {position}")

    dist = distance_3d(origin, position)
    print(f"Distance between {origin} & {position}: {dist}\n")

    print("Unpacking demonstration:")
    x, y, z = position
    print(f"Player at x={x}, y={y}, z={z}")
    print(f"Coordinates: X={x}, Y={y}, Z={z}\n")


if __name__ == "__main__":

    print("=== Game Coordinate System ===\n")

    origin = (0, 0, 0)
    man_position = (10, 20, 5)

    print(f"Manual example:\nPosition created: {man_position}")
    example_dist = distance_3d(origin, man_position)
    print(f"Distance between {origin} & {man_position}: {example_dist:.2f}\n")

    main("3,4,0", origin)
    main("abc,123,hij", origin)
