"""
This module contains utility functions for validating various inputs.
"""
def validate_required_fields(**kwargs):
    """
    Validates that all required fields have values.
    """
    for field_name, value in kwargs.items():
        if not value:
            raise ValueError(f"Missing required field: '{field_name}'")
