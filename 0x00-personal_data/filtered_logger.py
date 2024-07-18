#!/usr/bin/env python3
"""
Module to demonstrate user data and logging
"""
from os import getenv
import re
import logging
import mysql.connector
from typing import List, Optional


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
) -> str:
    """
    Function to filter data
    """
    patterns = [f"{field}=[^{separator}]*" for field in fields]

    combined_pattern = '|'.join(patterns)

    def substitute(match):
        """
        Helper function to get the substitue match
        """
        field_name = match.group(0).split('=')[0]

        return f"{field_name}={redaction}"

    result = re.sub(combined_pattern, substitute, message)

    return result


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialiazation methods
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format method
        """
        original_message = super().format(record)
        filtered_message = filter_datum(
                self.fields, self.REDACTION,
                original_message, self.SEPARATOR
        )

        return filtered_message


def get_logger() -> logging.Logger:
    """
    Get the logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a MySQL database connection
    """
    username = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=db_name
    )
