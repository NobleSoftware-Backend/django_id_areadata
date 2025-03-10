import csv
from functools import lru_cache
from pathlib import Path
from importlib import resources
from typing import Iterator, Type, Dict, List, Optional, cast, TypeVar, Union

from django_id_areadata.models import Area, District, Province, Regency, SubDistrict

# Create a type variable matching your model definition
AreaType = TypeVar("AreaType", bound=Area)

# Define the mapping with proper type annotations
MODEL_FILENAME_MAPPER: Dict[Type[Area], str] = {
    Province: "provinces.csv",
    Regency: "regencies.csv",
    District: "districts.csv",
    SubDistrict: "villages.csv",
}


def normalize_name(name: str) -> str:
    """Normalize area names with proper capitalization."""
    name = name.title()
    if "Dki" in name:
        name = name.replace("Dki", "DKI")
    return name


def build_model_items(
    model_class: Type[AreaType],
    data: Iterator[Dict[str, str]],
) -> List[AreaType]:
    """
    Build model instances from CSV data.

    Args:
        model_class: The area model class
        data: Iterator of dictionary rows from CSV

    Returns:
        List of model instances
    """
    results: List[AreaType] = []

    def get_parent_id(child_id: str) -> Optional[str]:
        model_names = list(MODEL_FILENAME_MAPPER.keys())
        model_index = model_names.index(model_class)

        if model_index == 0:  # Top-level model (Province) has no parent
            return None

        parent_parts = child_id.split(".")[:model_index]
        return ".".join(parent_parts) if parent_parts else None

    required_fields = ["code", "name"]

    for row in data:
        # Validate required fields, skip invalid rows
        if not all(field in row for field in required_fields):
            continue

        item = model_class(
            id=row["code"],
            name=normalize_name(row["name"]),
            parent_id=get_parent_id(row["code"]),
        )
        results.append(item)

    return results


@lru_cache(maxsize=4)  # Cache results for the 4 models
def read_csv(model_class: Type[AreaType]) -> List[AreaType]:
    """
    Read area data from CSV files and convert to model instances.

    Args:
        model_class: The area model class to read data for

    Returns:
        List of model instances

    Raises:
        ValueError: If an invalid model is provided or file mapping is missing
        FileNotFoundError: If the CSV file doesn't exist
    """
    if model_class not in MODEL_FILENAME_MAPPER:
        raise ValueError(
            f"Invalid model: {model_class.__name__}. "
            f"Expected one of: {', '.join(m.__name__ for m in MODEL_FILENAME_MAPPER)}"
        )

    file_name: str = MODEL_FILENAME_MAPPER.get(model_class)
    if file_name is None:
        raise ValueError(f"Cannot find the correct file for {model_class.__name__}.")

    file_path = resources.files("django_id_areadata.data").joinpath(file_name)
    if not file_path.is_file():
        raise FileNotFoundError(f"File {file_name} not found at {file_path}.")

    with file_path.open("r", encoding="utf-8") as file:
        csv_data = csv.DictReader(file)
        return build_model_items(model_class, csv_data)
