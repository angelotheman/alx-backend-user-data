#!/usr/bin/python3
"""
Module to demonstrate user data and logging
"""
import re
from typing import List


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

    def substitue(match):
        """
        Helper function to get the substitue match
        """
        field_name = match.group(0).split('=')[0]

        return f"{field_name}={redaction}"

    result = re.sub(combined_pattern, substitute, message)

    return result
