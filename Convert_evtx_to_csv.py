import argparse
import csv
import json
from datetime import datetime
from evtx import PyEvtxParser
from tqdm import tqdm
import os

LEVELDISPLAYNAMES = ["Severity Unknown", "Error", "Warning", "Information"]


def get_date(iso_string):
    """Convert ISO timestamp to formatted string."""
    try:
        iso_datetime = datetime.fromisoformat(iso_string.rstrip('Z'))
        return iso_datetime.strftime("%B %d, %Y %I:%M:%S %p UTC")
    except (ValueError, TypeError):
        return "N/A"


def find_message(event_data):
    """
    Recursively search for message-related fields in event data.
    Prioritize common fields like 'Message', 'Description', or '#text'.
    """

    def recursive_search(data, depth=0, max_depth=5):
        if depth > max_depth:
            return None
        if isinstance(data, dict):
            # Check for common message-related keys (case-insensitive)
            for key in data:
                if key.lower() in {'message', 'description', 'data', '#text', 'stringvalue', 'eventdescription'}:
                    if isinstance(data[key], str) and data[key].strip():
                        return data[key]
                    elif isinstance(data[key], list) and data[key] and isinstance(data[key][0], str):
                        return data[key][0]
                # Recurse into nested dictionaries
                result = recursive_search(data[key], depth + 1, max_depth)
                if result:
                    return result
        elif isinstance(data, list):
            # Check each item in the list
            for item in data:
                result = recursive_search(item, depth + 1, max_depth)
                if result:
                    return result
        return None

    # Start the recursive search
    message = recursive_search(event_data)

    if not message:
        # Fallback: try to get a generic representation of EventData
        event_data_section = event_data.get('Event', {}).get('EventData')
        if event_data_section:
            # Collect all string values in EventData
            strings = []

            def collect_strings(data):
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, str) and value.strip():
                            strings.append(f"{key}: {value}")
                        elif isinstance(value, (dict, list)):
                            collect_strings(value)
                elif isinstance(data, list):
                    for item in data:
                        collect_strings(item)

            collect_strings(event_data_section)
            if strings:
                return "; ".join(strings)

    return message or "No message found"


def extract_event_data(evtx_file, output_csv):
    """Extract event data from EVTX file and write to CSV."""
    try:
        parser = PyEvtxParser(evtx_file)
        with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["DateTime", "Severity", "Message", "Source"])

            for record in tqdm(parser.records_json(), desc="Processing records", unit="record"):
                try:
                    event_data = json.loads(record['data'])

                    # Extract timestamp
                    timestamp = event_data.get('Event', {}).get('System', {}).get('TimeCreated', {}).get('#attributes',
                                                                                                         {}).get(
                        'SystemTime', '')
                    formatted_time = get_date(timestamp)

                    # Extract severity
                    level = event_data.get('Event', {}).get('System', {}).get('Level', 0)
                    severity = LEVELDISPLAYNAMES[int(level) - 1] if 1 <= int(level) <= len(
                        LEVELDISPLAYNAMES) else "Unknown"

                    # Extract source
                    source = event_data.get('Event', {}).get('System', {}).get('Provider', {}).get('#attributes',
                                                                                                   {}).get('Name',
                                                                                                           'Unknown')

                    # Extract message
                    message = find_message(event_data)

                    writer.writerow([formatted_time, severity, message, source])
                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    # Log error but continue processing
                    print(f"Error processing record: {e}")
                    writer.writerow(
                        [formatted_time or "N/A", "Unknown", "Error parsing event data", source or "Unknown"])

        print(f"Data has been successfully written to {os.path.abspath(output_csv)}")
    except Exception as e:
        print(f"Error processing EVTX file: {e}")
        raise


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Extract event data from an EVTX file and write to a CSV file.")
    parser.add_argument("evtx_file", help="The path to the input EVTX file.")
    parser.add_argument("--output", default="Logs.csv", help="The path to the output CSV file (default: Logs.csv).")

    # Parse arguments
    args = parser.parse_args()
    extract_event_data(args.evtx_file, args.output)