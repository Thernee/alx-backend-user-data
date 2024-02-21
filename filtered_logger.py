#!/usr/bin/env python3

"""
filtered_logger.py
"""
import logging
import sys
import os
import re
import mysql.connector
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    filter_datum
    """
    
