import csv
import json
from datetime import datetime
from evtx import PyEvtxParser
print("Made it to here")
import xml.etree.ElementTree as Et


def extract_event_data(evtx_file, output_csv):
    parser = PyEvtxParser(evtx_file)
    for record in parser.records_json():
        print(f'Event Record ID: {record["event_record_id"]}')
        print(f'Event Timestamp: {record["timestamp"]}')
        print(record['data'])
        print(f'------------------------------------------')
    # with PyEvtxParser(evtx_file) as log:
    #     with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
    #         writer = csv.writer(csvfile)
    #         writer.writerow(["Severity", "Date and Time", "Description"])
    #
    #         for record in log.records():
    #             xml_str = evtx_file_xml_view(record)
    #             event_xml = Et.fromstring(xml_str)
    #
    #             # Extract relevant fields
    #             severity = event_xml.find(".//Level").text if event_xml.find(".//Level") is not None else "N/A"
    #             date_time = event_xml.find(".//TimeCreated").get("SystemTime") if event_xml.find(
    #                 ".//TimeCreated") is not None else "N/A"
    #             description = event_xml.find(".//EventData").text if event_xml.find(
    #                 ".//EventData") is not None else "N/A"
    #
    #             # Formatting date and time
    #             try:
    #                 date_time = datetime.fromisoformat(date_time.replace("Z", "+00:00"))
    #             except ValueError:
    #                 date_time = "N/A"
    #
    #             writer.writerow([severity, date_time, description])
    #
    # print(f"Data has been successfully written to {output_csv}")


input_evtx_file = r"test_files/sample.evtx"
output_csv_file = "output_events.csv"
extract_event_data(input_evtx_file, output_csv_file)
