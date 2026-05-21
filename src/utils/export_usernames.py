import json
import sys


def extract_usernames(data):
    """
    Extract usernames from the parsed JSON data.
    This function is kept separate to allow for easy modification if the JSON format changes.
    Handles two known formats:
    1. Array of objects with 'label_values' array containing objects with 'label' and 'value'.
    2. Object with key 'relationships_follow_requests_sent' containing array of items,
       each having 'string_list_data' array of objects with 'value'.
    """
    usernames = []
    
    # Format 2: Instagram style JSON
    if isinstance(data, dict) and "relationships_follow_requests_sent" in data:
        for item in data.get("relationships_follow_requests_sent", []):
            if isinstance(item, dict):
                for entry in item.get("string_list_data", []):
                    if isinstance(entry, dict) and "value" in entry:
                        usernames.append(entry.get("value"))
    
    # Format 1: Example style JSON (array of objects with label_values)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                label_values = item.get('label_values', [])
                if isinstance(label_values, list):
                    for label_obj in label_values:
                        if isinstance(label_obj, dict) and label_obj.get('label') == 'Username':
                            usernames.append(label_obj.get('value'))
                            break  # Assuming one username per item
    
    # If the format is unknown, return empty list (or could raise an error)
    return usernames


def main():
    if len(sys.argv) < 2:
        print("Usage: python export_usernames.py <path_to_json_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{file_path}': {e}")
        sys.exit(1)
    
    usernames = extract_usernames(data)
    # Output each username on a new line for easy processing
    for username in usernames:
        print(username)


if __name__ == '__main__':
    main()
