"""Query and aggregate rows in the MySQL ``mock`` table."""

import logging
import os
from typing import Any

import mysql.connector


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_COLUMNS = ("id", "group", "first_name", "age", "salary", "is_active")
GROUP_BY_QUERIES = {
    "id": "SELECT `id`, COUNT(*) AS count FROM mock GROUP BY `id` ORDER BY `id`",
    "group": "SELECT `group`, COUNT(*) AS count FROM mock GROUP BY `group` ORDER BY `group`",
    "first_name": (
        "SELECT `first_name`, COUNT(*) AS count FROM mock "
        "GROUP BY `first_name` ORDER BY `first_name`"
    ),
    "age": "SELECT `age`, COUNT(*) AS count FROM mock GROUP BY `age` ORDER BY `age`",
    "salary": (
        "SELECT `salary`, COUNT(*) AS count FROM mock "
        "GROUP BY `salary` ORDER BY `salary`"
    ),
    "is_active": (
        "SELECT `is_active`, COUNT(*) AS count FROM mock "
        "GROUP BY `is_active` ORDER BY `is_active`"
    ),
}


def _database_connection() -> Any:
    """Open a MySQL connection using database settings from environment variables."""
    logger.info("Connecting to the configured MySQL database")
    return mysql.connector.connect(
        host=os.environ["DBHOST"],
        database=os.environ["DBNAME"],
        user=os.environ["DBUSER"],
        password=os.environ["DBPASS"],
    )


def get_data_by_group(value: Any) -> list[tuple[Any, ...]]:
    """Return mock rows whose reserved ``group`` column equals ``value``."""
    query = (
        "SELECT id, `group`, first_name, age, salary, is_active "
        "FROM mock WHERE `group` = %s"
    )
    connection = None
    cursor = None
    try:
        logger.info("Querying mock rows for group %r", value)
        connection = _database_connection()
        cursor = connection.cursor()
        cursor.execute(query, (value,))
        rows = cursor.fetchall()
        logger.info("Found %d rows for group %r", len(rows), value)
        return rows
    except Exception:
        logger.exception("Unable to query mock rows by group")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def plot_counts(groupby: str) -> list[tuple[Any, ...]]:
    """Return counts grouped by an allowlisted mock column name."""
    logger.info("Preparing grouped count for %s", groupby)
    if groupby not in GROUP_BY_QUERIES:
        raise ValueError(f"Unsupported group-by column: {groupby}")

    connection = None
    cursor = None
    try:
        logger.info("Counting mock rows grouped by %s", groupby)
        connection = _database_connection()
        cursor = connection.cursor()
        cursor.execute(GROUP_BY_QUERIES[groupby])
        counts = cursor.fetchall()
        logger.info("Computed %d grouped counts", len(counts))
        return counts
    except Exception:
        logger.exception("Unable to compute grouped counts")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def main() -> None:
    """Demonstrate filtering and grouped counting for the mock table."""
    logger.info("Starting mock data query demonstrations")
    print(get_data_by_group("Engineering"))
    print(plot_counts("group"))


if __name__ == "__main__":
    main()
