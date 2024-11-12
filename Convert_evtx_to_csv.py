import argparse
import csv
import json
from datetime import datetime
from evtx import PyEvtxParser

LEVELDISPLAYNAMES = ["Warning", "Error", "Warning", "Information", "Unknown"]


# Formats date and time
def get_date(ISOString):
    try:
        IsoDateTime = datetime.fromisoformat(ISOString)
    except ValueError:
        date_time = "N/A"
    return IsoDateTime.strftime("%B %d, %Y %I:%M:%S %p UTC")


def extract_event_data(evtx_file, output_csv):
    parser = PyEvtxParser(evtx_file)
    with open(output_csv, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["DateTime", "Severity", "Message", "Source"])

        for record in parser.records_json():
            event_data = json.loads(record['data'])

            timestamp = get_date(event_data['Event']['System']['TimeCreated']['#attributes']['SystemTime'])
            severity = LEVELDISPLAYNAMES[event_data['Event']['System']['Level']-1]
            message = event_data['Event']['EventData']['Data']['#text'][0]
            program = event_data['Event']['System']['Provider']['#attributes']['Name']

            writer.writerow([timestamp, severity, message, program])
    print(f"Data has been successfully written to {output_csv}")


if __name__ == "__main__":
    # set up argument parsing
    parser = argparse.ArgumentParser(description="Extract event data from an EVTX file and write to a CSV file.")
    parser.add_argument("evtx_file", help="The path to the input EVTX file.")

    # Parse arguments
    args = parser.parse_args()

output_csv_file = "Logs.csv"
extract_event_data(args.evtx_file, output_csv_file)