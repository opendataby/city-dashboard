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

INSERT_CHUNK_SIZE = 1


def ensure_table_exists_stmt(name, columns):
    return 'CREATE TABLE IF NOT EXISTS {} ({})'.format(
        name,
        ', '.join(' '.join(item) for item in columns.items())
    )


def filter_row(data, known, wanted):
    return OrderedDict({
        key: data[key]
        for key in known
        if key in wanted
    })


def bulk_insert_stmt(table_name, keys, rows):
    values = (
        '({})'.format(', '.join(repr(data[key]) for key in keys))
        for data in rows
    )
    return 'INSERT INTO {} ({}) VALUES {}'.format(
        table_name,
        ', '.join(keys),
        ', '.join(values)
    )


def get_column_types(numeric_columns, default):
    data = defaultdict(lambda: default)
    for name in numeric_columns:
        data[name] = 'NUMERIC'

    return data


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description=__doc__)
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
    cmd_args = argparser.parse_args()

    logging_level = logging.DEBUG if cmd_args.verbose else logging.INFO
    logging.basicConfig(level=logging_level)
    logger = logging.getLogger('import')

    column_types = get_column_types(cmd_args.numeric.split(','), 'TEXT')
    columns = OrderedDict({
        name: column_types[name]
        for name in cmd_args.columns.split(',')
    })

    stream = sys.stdin if cmd_args.input == '-' else open(cmd_args.input)

    connection = sqlite3.connect(cmd_args.database)
    cursor = connection.cursor()
    logger.info('Connected to database %s', cmd_args.database)
    try:
        stmt = ensure_table_exists_stmt(cmd_args.table, columns)
        logger.debug('Hit query\n > %s', stmt)
        cursor.execute(stmt).fetchone()
        logger.info('Goind to write to %s table', cmd_args.table)

        reader = csv.DictReader(stream)
        logger.debug('Detected %d named csv-fields', len(reader.fieldnames))

        rows = (
            filter_row(row_dict, reader.fieldnames, columns)
            for row_dict in reader
        )
        stmt = bulk_insert_stmt(
            cmd_args.table,
            columns,
            rows
        )
        logger.debug('Hit query\n > %s', stmt)
        cursor.execute(stmt).fetchone()

        logger.info('Committing changes now')
        connection.commit()
    finally:
        logger.debug('Closing db connection')
        connection.close()
