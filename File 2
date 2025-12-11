"""
CSV Handler Module for ViralTrendAgent

This module provides a robust CSV handler with error handling, data validation,
and logging capabilities for the ViralTrendAgent script.

Features:
- CSV file reading and writing with error handling
- Data validation and type checking
- Comprehensive logging for debugging and monitoring
- Support for custom delimiters and encodings
- Automatic backup creation before overwriting
- Data consistency checks
"""

import csv
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple


class CSVHandlerException(Exception):
    """Base exception for CSV handler errors."""
    pass


class CSVValidationError(CSVHandlerException):
    """Exception raised for data validation errors."""
    pass


class CSVIOError(CSVHandlerException):
    """Exception raised for file I/O errors."""
    pass


class CSVHandler:
    """
    A robust CSV handler for reading, writing, and validating CSV files
    with comprehensive error handling and logging.
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        encoding: str = 'utf-8',
        delimiter: str = ',',
        create_backups: bool = True
    ):
        """
        Initialize the CSV handler.

        Args:
            logger: Logger instance for logging operations. If None, creates a new logger.
            encoding: File encoding to use (default: 'utf-8').
            delimiter: CSV delimiter character (default: ',').
            create_backups: Whether to create backups before overwriting files (default: True).
        """
        self.logger = logger or self._setup_logger()
        self.encoding = encoding
        self.delimiter = delimiter
        self.create_backups = create_backups

        self.logger.info(
            f"CSVHandler initialized with encoding={encoding}, delimiter='{delimiter}', "
            f"create_backups={create_backups}"
        )

    @staticmethod
    def _setup_logger() -> logging.Logger:
        """Set up a default logger for CSV operations."""
        logger = logging.getLogger('CSVHandler')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def read_csv(
        self,
        file_path: str,
        expected_columns: Optional[List[str]] = None,
        skip_validation: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Read and parse a CSV file with validation.

        Args:
            file_path: Path to the CSV file.
            expected_columns: List of expected column names for validation.
            skip_validation: Skip column validation if True.

        Returns:
            List of dictionaries representing CSV rows.

        Raises:
            CSVIOError: If file cannot be read.
            CSVValidationError: If validation fails.
        """
        try:
            file_path = Path(file_path)

            if not file_path.exists():
                raise CSVIOError(f"File not found: {file_path}")

            if not file_path.is_file():
                raise CSVIOError(f"Path is not a file: {file_path}")

            self.logger.info(f"Reading CSV file: {file_path}")

            data = []
            with open(file_path, 'r', encoding=self.encoding, newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=self.delimiter)

                if reader.fieldnames is None:
                    raise CSVValidationError("CSV file is empty or has no headers")

                # Validate columns
                if expected_columns and not skip_validation:
                    self._validate_columns(reader.fieldnames, expected_columns)

                for row_num, row in enumerate(reader, start=2):
                    try:
                        cleaned_row = {k: v for k, v in row.items() if k is not None}
                        data.append(cleaned_row)
                    except Exception as e:
                        self.logger.warning(f"Error parsing row {row_num}: {str(e)}")
                        raise CSVValidationError(f"Error parsing row {row_num}: {str(e)}")

            self.logger.info(f"Successfully read {len(data)} rows from {file_path}")
            return data

        except (CSVIOError, CSVValidationError):
            raise
        except Exception as e:
            error_msg = f"Unexpected error reading CSV file {file_path}: {str(e)}"
            self.logger.error(error_msg)
            raise CSVIOError(error_msg) from e

    def write_csv(
        self,
        file_path: str,
        data: List[Dict[str, Any]],
        overwrite: bool = True,
        validate_before_write: bool = True
    ) -> None:
        """
        Write data to a CSV file with validation and backup support.

        Args:
            file_path: Path where the CSV file should be written.
            data: List of dictionaries to write as CSV rows.
            overwrite: Whether to overwrite existing files (default: True).
            validate_before_write: Validate data before writing (default: True).

        Raises:
            CSVIOError: If file cannot be written.
            CSVValidationError: If validation fails or data is invalid.
        """
        try:
            file_path = Path(file_path)

            if not data:
                raise CSVValidationError("Cannot write empty data list")

            # Validate data structure
            if validate_before_write:
                self._validate_data_structure(data)

            # Check if file exists and handle backup
            if file_path.exists() and not overwrite:
                raise CSVIOError(
                    f"File already exists and overwrite is False: {file_path}"
                )

            if file_path.exists() and self.create_backups:
                self._create_backup(file_path)

            # Create parent directories if they don't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)

            self.logger.info(f"Writing {len(data)} rows to {file_path}")

            # Get all unique fieldnames
            fieldnames = list(data[0].keys())

            with open(file_path, 'w', encoding=self.encoding, newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=self.delimiter)
                writer.writeheader()
                writer.writerows(data)

            self.logger.info(f"Successfully wrote {len(data)} rows to {file_path}")

        except (CSVIOError, CSVValidationError):
            raise
        except Exception as e:
            error_msg = f"Unexpected error writing CSV file {file_path}: {str(e)}"
            self.logger.error(error_msg)
            raise CSVIOError(error_msg) from e

    def append_csv(
        self,
        file_path: str,
        data: List[Dict[str, Any]],
        validate: bool = True
    ) -> None:
        """
        Append data to an existing CSV file.

        Args:
            file_path: Path to the CSV file.
            data: List of dictionaries to append.
            validate: Validate data before appending (default: True).

        Raises:
            CSVIOError: If file cannot be appended to.
            CSVValidationError: If validation fails.
        """
        try:
            file_path = Path(file_path)

            if not data:
                raise CSVValidationError("Cannot append empty data list")

            if validate:
                self._validate_data_structure(data)

            if not file_path.exists():
                raise CSVIOError(f"File does not exist: {file_path}")

            self.logger.info(f"Appending {len(data)} rows to {file_path}")

            with open(file_path, 'a', encoding=self.encoding, newline='') as csvfile:
                if file_path.stat().st_size == 0:
                    fieldnames = list(data[0].keys())
                    writer = csv.DictWriter(
                        csvfile, fieldnames=fieldnames, delimiter=self.delimiter
                    )
                    writer.writeheader()
                    writer.writerows(data)
                else:
                    fieldnames = list(data[0].keys())
                    writer = csv.DictWriter(
                        csvfile, fieldnames=fieldnames, delimiter=self.delimiter
                    )
                    writer.writerows(data)

            self.logger.info(f"Successfully appended {len(data)} rows to {file_path}")

        except (CSVIOError, CSVValidationError):
            raise
        except Exception as e:
            error_msg = f"Unexpected error appending to CSV file {file_path}: {str(e)}"
            self.logger.error(error_msg)
            raise CSVIOError(error_msg) from e

    def validate_csv(
        self,
        file_path: str,
        expected_columns: Optional[List[str]] = None,
        max_file_size_mb: float = 100.0
    ) -> Tuple[bool, List[str]]:
        """
        Validate a CSV file without loading all data into memory.

        Args:
            file_path: Path to the CSV file.
            expected_columns: Expected column names.
            max_file_size_mb: Maximum file size in MB.

        Returns:
            Tuple of (is_valid, list_of_errors).
        """
        errors = []
        file_path = Path(file_path)

        try:
            if not file_path.exists():
                return False, [f"File not found: {file_path}"]

            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            if file_size_mb > max_file_size_mb:
                errors.append(f"File size ({file_size_mb:.2f} MB) exceeds limit ({max_file_size_mb} MB)")

            with open(file_path, 'r', encoding=self.encoding, newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=self.delimiter)

                if reader.fieldnames is None:
                    return False, ["CSV file is empty or has no headers"]

                if expected_columns:
                    missing = set(expected_columns) - set(reader.fieldnames or [])
                    if missing:
                        errors.append(f"Missing expected columns: {missing}")

                for i, row in enumerate(reader):
                    if i >= 100:
                        break
                    if not row or all(v is None or v == '' for v in row.values()):
                        errors.append(f"Empty row found at line {i + 2}")

            if errors:
                self.logger.warning(f"CSV validation found {len(errors)} issue(s): {errors}")
                return False, errors

            self.logger.info(f"CSV validation passed for {file_path}")
            return True, []

        except Exception as e:
            error_msg = f"Error validating CSV file: {str(e)}"
            self.logger.error(error_msg)
            return False, [error_msg]

    @staticmethod
    def _validate_columns(actual_columns: Tuple[str, ...], expected_columns: List[str]) -> None:
        """Validate that all expected columns are present."""
        actual_set = set(actual_columns)
        expected_set = set(expected_columns)
        missing = expected_set - actual_set

        if missing:
            raise CSVValidationError(
                f"Missing expected columns: {missing}. "
                f"Found columns: {actual_set}"
            )

    @staticmethod
    def _validate_data_structure(data: List[Dict[str, Any]]) -> None:
        """Validate the structure of data before writing."""
        if not isinstance(data, list):
            raise CSVValidationError("Data must be a list of dictionaries")

        if not data:
            raise CSVValidationError("Data list cannot be empty")

        if not isinstance(data[0], dict):
            raise CSVValidationError("Each row in data must be a dictionary")

        first_keys = set(data[0].keys())
        for i, row in enumerate(data):
            if not isinstance(row, dict):
                raise CSVValidationError(f"Row {i} is not a dictionary")
            if not set(row.keys()).issubset(first_keys):
                raise CSVValidationError(
                    f"Row {i} has keys {set(row.keys())} that are not in first row {first_keys}"
                )

    @staticmethod
    def _create_backup(file_path: Path) -> None:
        """Create a backup of the file before overwriting."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = file_path.parent / f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
        shutil.copy2(file_path, backup_path)


def get_csv_handler(
    encoding: str = 'utf-8',
    delimiter: str = ',',
    create_backups: bool = True,
    log_level: str = 'INFO'
) -> CSVHandler:
    """Factory function to create a configured CSV handler instance."""
    logger = logging.getLogger('CSVHandler')
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    return CSVHandler(
        logger=logger,
        encoding=encoding,
        delimiter=delimiter,
        create_backups=create_backups
    )
