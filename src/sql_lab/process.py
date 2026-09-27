"""Clean CSV data and load it into the MySQL ``mock`` table."""

import logging
import os
from typing import Any

import mysql.connector
import pandas as pd


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_COLUMNS = ("id", "group", "first_name", "age", "salary", "is_active")


def read_data(filename: str) -> pd.DataFrame:
    """Read ``filename`` into a pandas DataFrame."""
    logger.info("Reading data from %s", filename)
    data = pd.read_csv(filename)
    logger.info("Read %d rows", len(data))
    return data


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with every row containing a missing field removed."""
    logger.info("Cleaning %d rows", len(data))
    cleaned = data.copy()

    # Treat empty or whitespace-only CSV fields as missing values as well.
    cleaned = cleaned.replace(r"^\s*$", pd.NA, regex=True)
    cleaned = cleaned.dropna(axis=0, how="any").copy()
    logger.info("Retained %d rows after removing incomplete records", len(cleaned))
    return cleaned


def _database_connection() -> Any:
    """Open a MySQL connection using database settings from environment variables."""
    logger.info("Connecting to the configured MySQL database")
    return mysql.connector.connect(
        host=os.environ["DBHOST"],
        database=os.environ["DBNAME"],
        user=os.environ["DBUSER"],
        password=os.environ["DBPASS"],
    )


def _to_python_value(value: Any) -> Any:
    """Convert pandas or NumPy scalar values into connector-compatible Python values."""
    logger.debug("Converting database value of type %s", type(value).__name__)
    return value.item() if hasattr(value, "item") else value


def load_data(data: pd.DataFrame, table: str) -> None:
    """Upsert ``data`` into the fixed ``mock`` table using parameterized values."""
    logger.info("Preparing to load %d rows into %s", len(data), table)
    if table != "mock":
        raise ValueError("load_data only supports the mock table")

    create_table = """
        CREATE TABLE IF NOT EXISTS mock (
            id BIGINT PRIMARY KEY,
            `group` VARCHAR(255) NOT NULL,
            first_name VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            salary DOUBLE NOT NULL,
            is_active TINYINT(1) NOT NULL
        )
    """
    upsert = """
        INSERT INTO mock
            (`id`, `group`, `first_name`, `age`, `salary`, `is_active`)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            `group` = VALUES(`group`),
            first_name = VALUES(first_name),
            age = VALUES(age),
            salary = VALUES(salary),
            is_active = VALUES(is_active)
    """

    connection = None
    cursor = None
    try:
        logger.info("Loading %d rows into mock", len(data))
        connection = _database_connection()
        cursor = connection.cursor()
        cursor.execute(create_table)

        # Select the documented schema explicitly so upload order is deterministic.
        for row in data.loc[:, DATA_COLUMNS].itertuples(index=False, name=None):
            values = tuple(_to_python_value(value) for value in row)
            cursor.execute(upsert, values)
        connection.commit()
        logger.info("Upserted %d rows into mock", len(data))
    except Exception:
        logger.exception("Unable to load data into mock")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def main() -> None:
    """Read, clean, and upsert ``MOCK_DATA.csv`` into the mock table."""
    logger.info("Starting mock data processing")
    data = read_data("MOCK_DATA.csv")
    cleaned = clean_data(data)
    load_data(cleaned, "mock")


if __name__ == "__main__":
    main()
