#!/usr/bin/env python3
"""
Opendata csv to sqlite3 importer.
This script allows to convert csv-stream to rows in sqlite table
"""

import argparse
import csv
import itertools
import logging
import os
import sqlite3
import sys
from collections import (
    defaultdict,
    OrderedDict,
)


def ensure_table_exists_stmt(table_name, columns):
    return 'CREATE TABLE IF NOT EXISTS {} ({})'.format(
        table_name,
        ', '.join(' '.join(name_and_affinity) for name_and_affinity in columns.items())
    )


def insert_stmt(table_name, keys):
    placeholders = ', '.join(':{}'.format(key) for key in keys)
    return 'INSERT INTO {} ({}) VALUES {}'.format(
        table_name,
        ', '.join(keys),
        '({})'.format(placeholders)
    )


def get_column_types(numeric_columns, default):
    data = defaultdict(lambda: default)
    for name in numeric_columns:
        data[name] = 'NUMERIC'

    return data


def get_columns(column_names, numeric_columns):
    columns = OrderedDict()
    column_types = get_column_types(numeric_columns, 'TEXT')
    for name in column_names:
        columns[name] = column_types[name]
    return columns


def parse_args(description):
    argparser = argparse.ArgumentParser(description=description)
    argparser.add_argument('-v', action='store_true', dest='verbose', help='Verbose logging to console')
    argparser.add_argument('database', action='store', help='Filename of sqlite3 database to connect')
    argparser.add_argument('table', action='store', help='Table name to save rows to')
    argparser.add_argument(
        '-c',
        action='store',
        dest='columns',
        help='Comma separated list of columns of interest',
    )
    argparser.add_argument(
        '-n',
        action='store',
        dest='numeric',
        default=[],
        help='Comma separated list of columns with numeric values. It may contain integers or doubles',
    )
    argparser.add_argument('input', action='store', help='Data stream to read. Filename or "-" for stdin')
    return argparser.parse_args()


def get_logger(logging_level):
    logging.basicConfig(level=logging_level)
    return logging.getLogger('import')


if __name__ == '__main__':
    cmd_args = parse_args(__doc__)
    logger = get_logger(logging.DEBUG if cmd_args.verbose else logging.INFO)

    stream = sys.stdin if cmd_args.input == '-' else open(cmd_args.input)
    reader = csv.DictReader(stream)
    logger.info('Detected %d named csv-fields total', len(reader.fieldnames))

    connection = sqlite3.connect(cmd_args.database)
    cursor = connection.cursor()
    logger.info('Connected to database %s', cmd_args.database)

    columns = get_columns(cmd_args.columns.split(','), cmd_args.numeric.split(','))

    try:
        stmt = ensure_table_exists_stmt(cmd_args.table, columns)
        logger.debug('Hit query\n > %s', stmt)
        cursor.execute(stmt)
        logger.info('Going to write to %s table', cmd_args.table)

        stmt = insert_stmt(cmd_args.table, columns)
        logger.debug('Hit queries\n > %s', stmt)
        result = cursor.executemany(stmt, reader)

        logger.debug('Committing changes now')
        connection.commit()
    finally:
        logger.debug('Closing db connection')
        connection.close()
