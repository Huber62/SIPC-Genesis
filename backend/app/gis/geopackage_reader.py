from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]
GIS_DATA_DIR = PROJECT_ROOT / "gis" / "data"

EXPECTED_FILES = (
    "250520_CdO_z_base_LST.gpkg",
    "260727_CdO_z_sovrapposta_LST.gpkg",
    "CdO_BC_Agra_Gent_Mont.gpkg",
    "CdO_BC_Carabietta.gpkg",
    "CdO_Beni_immobili.gpkg",
    "CdO_copertura_suolo.gpkg",
)


class GeoPackageReadError(RuntimeError):
    """Errore controllato durante la lettura di un GeoPackage."""


def _connect(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise GeoPackageReadError(f"File non trovato: {path.name}")

    try:
        connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as exc:
        raise GeoPackageReadError(
            f"Impossibile aprire {path.name}: {exc}"
        ) from exc


def _table_columns(
    connection: sqlite3.Connection,
    table_name: str,
) -> list[dict[str, Any]]:
    safe_name = table_name.replace('"', '""')
    rows = connection.execute(
        f'PRAGMA table_info("{safe_name}")'
    ).fetchall()

    return [
        {
            "name": row["name"],
            "type": row["type"],
            "required": bool(row["notnull"]),
            "primary_key": bool(row["pk"]),
        }
        for row in rows
    ]


def _feature_count(
    connection: sqlite3.Connection,
    table_name: str,
) -> int:
    safe_name = table_name.replace('"', '""')
    row = connection.execute(
        f'SELECT COUNT(*) AS total FROM "{safe_name}"'
    ).fetchone()
    return int(row["total"])


def inspect_geopackage(path: Path) -> dict[str, Any]:
    with _connect(path) as connection:
        layer_rows = connection.execute(
            """
            SELECT
                c.table_name,
                c.identifier,
                c.description,
                c.data_type,
                c.srs_id,
                g.geometry_type_name,
                g.column_name AS geometry_column
            FROM gpkg_contents AS c
            LEFT JOIN gpkg_geometry_columns AS g
                ON g.table_name = c.table_name
            WHERE c.data_type = 'features'
            ORDER BY c.table_name
            """
        ).fetchall()

        layers: list[dict[str, Any]] = []

        for row in layer_rows:
            table_name = str(row["table_name"])

            layers.append(
                {
                    "table_name": table_name,
                    "identifier": row["identifier"],
                    "description": row["description"],
                    "srs_id": row["srs_id"],
                    "geometry_type": row["geometry_type_name"],
                    "geometry_column": row["geometry_column"],
                    "feature_count": _feature_count(
                        connection,
                        table_name,
                    ),
                    "columns": _table_columns(
                        connection,
                        table_name,
                    ),
                }
            )

        return {
            "filename": path.name,
            "size_mb": round(
                path.stat().st_size / (1024 * 1024),
                2,
            ),
            "available": True,
            "layers": layers,
        }


def inspect_all_geopackages() -> dict[str, Any]:
    datasets: list[dict[str, Any]] = []

    for filename in EXPECTED_FILES:
        path = GIS_DATA_DIR / filename

        try:
            datasets.append(inspect_geopackage(path))
        except GeoPackageReadError as exc:
            datasets.append(
                {
                    "filename": filename,
                    "available": False,
                    "error": str(exc),
                    "layers": [],
                }
            )

    available = sum(
        bool(dataset["available"])
        for dataset in datasets
    )

    return {
        "directory": str(GIS_DATA_DIR),
        "expected": len(EXPECTED_FILES),
        "available": available,
        "missing_or_invalid": len(EXPECTED_FILES) - available,
        "ready": available == len(EXPECTED_FILES),
        "datasets": datasets,
    }
