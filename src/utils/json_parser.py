import json
import ast
import re
from typing import Any


def json_parser(input_string: str) -> Any:
    def extract_json_block(text):
        """Extract JSON content from a ```json code block."""
        match = re.search(r"```json(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text  # If no code block, return original string

    # Step 1: Clean the input
    cleaned_input = extract_json_block(input_string)

    # Step 2: Try JSON decoding
    try:
        parsed = json.loads(cleaned_input)
        if isinstance(parsed, (dict, list)):
            return parsed
    except json.JSONDecodeError:
        pass

    # Step 3: Try ast.literal_eval
    try:
        python_dict = ast.literal_eval(cleaned_input)
        json_string = json.dumps(python_dict)
        parsed = json.loads(json_string)
        if isinstance(parsed, (dict, list)):
            return parsed
    except (ValueError, SyntaxError):
        pass

    raise ValueError("Invalid JSON or Python literal or formatted block")
