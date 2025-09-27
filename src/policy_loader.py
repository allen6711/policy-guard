import json
import os
from jsonschema import validate

class PolicyError(Exception):
    """Custom exception for policy loading errors."""
    pass

def load_and_validate_policy(policy_path: str) -> dict:
    """
    Loads a JSON policy file and validates it against the schema.

    Args:
        policy_path: The path to the policy JSON file.

    Returns:
        The validated policy as a dictionary.

    Raises:
        PolicyError: If the file cannot be found, is invalid JSON, or fails schema validation.
    """
    # Define the path to the schema file relative to this script
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'policies', 'policy_schema.json')

    if not os.path.exists(schema_path):
        raise PolicyError(f"Schema file not found at {schema_path}")
    if not os.path.exists(policy_path):
        raise PolicyError(f"Policy file not found at {policy_path}")

    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        with open(policy_path, 'r') as f:
            policy = json.load(f)
    except json.JSONDecodeError as e:
        raise PolicyError(f"Invalid JSON in file: {e}")

    try:
        validate(instance=policy, schema=schema)
        return policy
    except Exception as e:
        raise PolicyError(f"Policy validation failed: {e}")