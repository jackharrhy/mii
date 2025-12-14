#!/usr/bin/env python3
"""
Example usage of the mii library for programmatic Mii file extraction and analysis

This demonstrates how to use the library without the CLI interface.
The library works entirely in-memory - no disk I/O unless you explicitly write files.
"""

from pathlib import Path
from mii import (
    MiiDatabase,
    MiiParser,
    MiiType,
    MiiDatabaseError,
)


def example_load_database():
    """Example: Load Miis from a database file into memory"""
    print("=" * 60)
    print("Example 1: Loading Miis from Wii Plaza database")
    print("=" * 60)

    input_file = Path("RFL_DB.dat")

    try:
        source_file = (
            input_file if input_file.exists() else Path(MiiType.WII_PLAZA.SOURCE)
        )
        database = MiiDatabase(source_file, MiiType.WII_PLAZA)

        print(f"Successfully loaded {len(database)} Miis into memory")
        print(f"Database type: {database.mii_type.display_name}")
        print(f"Source file: {database.file_path}")

        print("\nFirst 3 Miis:")
        for idx, mii in enumerate(database):
            if idx >= 3:
                break
            print(f"  {idx}: {mii.name} by {mii.creator_name}")

    except MiiDatabaseError as e:
        print(f"Loading failed: {e}")


def example_work_with_mii_objects():
    """Example: Work with Mii dataclass objects"""
    print("\n" + "=" * 60)
    print("Example 2: Working with Mii objects")
    print("=" * 60)

    try:
        database = MiiDatabase(Path(MiiType.WII_PLAZA.SOURCE), MiiType.WII_PLAZA)
    except MiiDatabaseError:
        print("Note: Database file not found. Skipping this example.")
        return

    if len(database) == 0:
        print("No Miis found in database")
        return

    mii = database[0]

    print(f"Mii Name: {mii.name}")
    print(f"Creator: {mii.creator_name}")
    print(f"Mii ID: {mii.get_mii_id_hex()}")
    print(f"Gender: {mii.get_gender_string()}")
    print(f"Birthday: {mii.get_birthday_string()}")
    print(f"Favorite Color: {mii.favorite_color}")
    print(f"Is Favorite: {mii.is_favorite}")

    print(f"\nRaw data size: {len(mii.raw_data)} bytes")
    print(f"With padding: {len(mii.to_bytes())} bytes")


def example_iterate_and_filter():
    """Example: Iterate and filter Miis"""
    print("\n" + "=" * 60)
    print("Example 3: Iterating and filtering Miis")
    print("=" * 60)

    try:
        database = MiiDatabase(Path(MiiType.WII_PLAZA.SOURCE), MiiType.WII_PLAZA)
    except MiiDatabaseError:
        print("Note: Database file not found. Skipping this example.")
        return

    print(f"Total Miis: {len(database)}")

    favorites = database.get_favorites()
    print(f"Favorite Miis: {len(favorites)}")

    red_miis = database.filter(lambda m: m.favorite_color == "Red")
    print(f"Red favorite color Miis: {len(red_miis)}")

    named_miis = database.filter(lambda m: m.name and m.name != "Unnamed")
    print(f"Named Miis: {len(named_miis)}")

    if red_miis:
        print("\nFirst Red Miis:")
        for mii in red_miis[:3]:
            print(f"  {mii.name} by {mii.creator_name}")


def example_parse_single_file():
    """Example: Parse a single Mii file"""
    print("\n" + "=" * 60)
    print("Example 4: Parsing a single Mii file")
    print("=" * 60)

    mii_file = Path("./extracted_miis/WII_PL00000.mii")

    if not mii_file.exists():
        print(f"Note: {mii_file} does not exist.")
        print("Extract some Miis first using the CLI or write them programmatically.")
        return

    try:
        with open(mii_file, "rb") as f:
            mii_data = f.read()

        mii = MiiParser.parse(mii_data)

        print(f"Mii Name: {mii.name}")
        print(f"Creator: {mii.creator_name}")
        print(f"Gender: {mii.get_gender_string()}")
        print(f"Birthday: {mii.get_birthday_string()}")
        print(f"Favorite Color: {mii.favorite_color}")
        print(f"Mii ID: {mii.get_mii_id_hex()}")

    except Exception as e:
        print(f"Error reading Mii file: {e}")


def example_write_miis_to_disk():
    """Example: Write Miis from database to disk files"""
    print("\n" + "=" * 60)
    print("Example 5: Writing Miis to disk")
    print("=" * 60)

    output_dir = Path("./extracted_miis")

    try:
        database = MiiDatabase(Path(MiiType.WII_PLAZA.SOURCE), MiiType.WII_PLAZA)
    except MiiDatabaseError:
        print("Note: Database file not found. Skipping this example.")
        return

    exported_paths = database.export_all(output_dir)
    print(f"Wrote {len(exported_paths)} Miis to {output_dir}")

    # Example: Export a single Mii
    if len(database) > 0:
        single_mii_path = output_dir / "single_mii.mii"
        database[0].export(single_mii_path)
        print(f"Also exported single Mii to {single_mii_path}")


def example_timestamps():
    """Example: Extract and display creation timestamps"""
    print("\n" + "=" * 60)
    print("Example 6: Extracting creation timestamps")
    print("=" * 60)

    mii_directory = Path("./extracted_miis")
    mii_files = list(mii_directory.glob("*.mii"))

    if not mii_files:
        print(f"No .mii files found in {mii_directory}")
        return

    print(f"Analyzing timestamps for {len(mii_files)} files...\n")

    for mii_file in sorted(mii_files)[:5]:  # Show first 5
        try:
            with open(mii_file, "rb") as f:
                mii_data = f.read()
            mii = MiiParser.parse(mii_data)

            creation_time = mii.get_creation_datetime()
            mii_type = "Wii" if mii.is_wii_mii else "3DS/WiiU"
            print(f"{mii_file.name}:")
            print(f"  Type: {mii_type}")
            print(f"  Creation Time: {creation_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print()

        except Exception as e:
            print(f"Error analyzing {mii_file.name}: {e}")


def example_error_handling():
    """Example: Proper error handling"""
    print("\n" + "=" * 60)
    print("Example 7: Error handling")
    print("=" * 60)

    # Try to load from a non-existent file
    try:
        database = MiiDatabase(Path("nonexistent.dat"), MiiType.WII_PLAZA)
    except MiiDatabaseError as e:
        print(f"Caught expected error: {e}")

    # Try to parse invalid data
    try:
        mii = MiiParser.parse(b"invalid data")
    except Exception as e:
        print(f"Caught expected parsing error: {e}")


def example_custom_processing():
    """Example: Custom processing pipeline with in-memory data"""
    print("\n" + "=" * 60)
    print("Example 8: Custom processing pipeline")
    print("=" * 60)

    try:
        database = MiiDatabase(Path(MiiType.WII_PLAZA.SOURCE), MiiType.WII_PLAZA)
    except MiiDatabaseError:
        print("Note: Database file not found. Skipping this example.")
        return

    # Process Miis in memory without writing to disk
    red_miis = database.filter(lambda m: m.favorite_color == "Red")
    favorite_miis = database.filter(lambda m: m.is_favorite)
    named_miis = database.filter(lambda m: m.name and m.name != "Unnamed")

    print(f"Total Miis: {len(database)}")
    print(f"Red favorite color: {len(red_miis)}")
    print(f"Favorites: {len(favorite_miis)}")
    print(f"Named: {len(named_miis)}")

    # Find Miis by creator
    creator_miis = {}
    for mii in database:
        if mii.creator_name and mii.creator_name != "Unknown":
            creator_miis.setdefault(mii.creator_name, []).append(mii.name)

    print(f"\nCreators: {len(creator_miis)}")
    for creator, names in list(creator_miis.items())[:3]:
        print(f"  {creator}: {len(names)} Miis")


def example_multiple_databases():
    """Example: Work with multiple database types"""
    print("\n" + "=" * 60)
    print("Example 9: Working with multiple database types")
    print("=" * 60)

    databases = {}
    total_miis = 0

    for mii_type in MiiType:
        try:
            database = MiiDatabase(Path(mii_type.SOURCE), mii_type)
            databases[mii_type.display_name] = database
            total_miis += len(database)
            print(f"{mii_type.display_name}: {len(database)} Miis")
        except MiiDatabaseError:
            print(f"{mii_type.display_name}: Not found")

    print(f"\nTotal Miis across all databases: {total_miis}")

    # Combine Miis from different databases
    if databases:
        all_miis = []
        for db in databases.values():
            all_miis.extend(db.get_all())

        print(f"\nCombined total: {len(all_miis)} unique Miis")


if __name__ == "__main__":
    print("Mii Library Usage Examples")
    print("=" * 60)
    print("\nNote: Some examples require database files.")
    print("Place RFL_DB.dat, FFL_ODB.dat, or CFL_DB.dat in the current directory.\n")

    # Run examples
    example_load_database()
    example_work_with_mii_objects()
    example_iterate_and_filter()
    example_parse_single_file()
    example_write_miis_to_disk()
    example_timestamps()
    example_error_handling()
    example_custom_processing()
    example_multiple_databases()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
