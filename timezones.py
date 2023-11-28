import argparse
import json
from tabulate import tabulate

class TimeZone:
    def __init__(self, data):
        self.data = data
        self.timezones = self.load_timezones()

    def load_timezones(self):
        try:
            with open(self.data, 'r') as file:
                return json.load(file)
        except FileNotFoundError as error:
            print(f"Error: Unable to load data from {self.data_file} - {error}")
            return []

    def filter_timezones(self, match=None, offset=None):
        filtered_timezones = []

        for tz in self.timezones:
            if (match is None or match in tz['value']) and (offset is None or offset == tz['offset']):
                filtered_timezones.append(tz)

        return filtered_timezones

    def display_timezones(self, timezones):
        headers = ["Value", "Abbr", "Offset", "Is DST"]
        table_data = [(tz["value"], tz["abbr"], tz["offset"], tz["isdst"]) for tz in timezones]

        if table_data:
            print(tabulate(table_data, headers, tablefmt="grid"))
        else:
            print("No matching time zones found.")

def main():
    parser = argparse.ArgumentParser(description="World Time Zones Information")
    parser.add_argument("--match", help="Filter time zones by value")
    parser.add_argument("--offset", nargs="?",help="Filter time zones by offset")
    args = parser.parse_args()

    timezone_info = TimeZone("timezones.json")
    filtered_timezones = timezone_info.filter_timezones(args.match, args.offset)
    timezone_info.display_timezones(filtered_timezones)

if __name__ == "__main__":
    main()

