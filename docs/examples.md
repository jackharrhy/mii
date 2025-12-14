# Examples

## Loading a Database

```python
from pathlib import Path
from mii import MiiDatabase, MiiType

database = MiiDatabase(Path("RFL_DB.dat"), MiiType.WII_PLAZA)
print(f"Loaded {len(database)} Miis")
```

## Working with Mii Objects

```python
mii = database[0]

print(f"Mii Name: {mii.name}")
print(f"Creator: {mii.creator_name}")
print(f"Gender: {mii.get_gender_string()}")
print(f"Birthday: {mii.get_birthday_string()}")
print(f"Favorite Color: {mii.favorite_color}")
print(f"Mii ID: {mii.get_mii_id_hex()}")
```

## Iterating and Filtering

```python
# Iterate over all Miis
for mii in database:
    print(f"{mii.name} by {mii.creator_name}")

# Get favorite Miis
favorites = database.get_favorites()

# Filter by color
red_miis = database.filter(lambda m: m.favorite_color == "Red")

# Filter by name
named_miis = database.filter(lambda m: m.name and m.name != "Unnamed")

# Find by name
mii = database.get_by_name("My Mii")
```

## Parsing Individual Files

```python
from mii import MiiParser

with open("WII_PL00000.mii", "rb") as f:
    mii_data = f.read()

mii = MiiParser.parse(mii_data)
print(mii.name)
print(mii.get_creation_datetime())
```

## Exporting Miis

```python
from pathlib import Path

# Export all Miis to a directory
output_dir = Path("./extracted_miis")
exported_paths = database.export_all(output_dir)

# Export a single Mii
mii.export(Path("./my_mii.mii"))
```

## Working with Multiple Database Types

```python
from mii import MiiDatabase, MiiType

databases = {}
for mii_type in MiiType:
    try:
        db = MiiDatabase(Path(mii_type.SOURCE), mii_type)
        databases[mii_type.display_name] = db
        print(f"{mii_type.display_name}: {len(db)} Miis")
    except MiiDatabaseError:
        print(f"{mii_type.display_name}: Not found")
```

## Error Handling

```python
from mii import MiiDatabase, MiiDatabaseError, MiiType

try:
    database = MiiDatabase(Path("nonexistent.dat"), MiiType.WII_PLAZA)
except MiiDatabaseError as e:
    print(f"Error: {e}")
```

## Accessing Creation Timestamps

```python
mii = database[0]
creation_time = mii.get_creation_datetime()
print(f"Created: {creation_time.strftime('%Y-%m-%d %H:%M:%S')}")
```

---

For more detailed examples, see the [complete examples file](https://github.com/jackharrhy/mii/examples/library_usage.py).
