import json
import argparse
import requests
import tabulate

class TimeZoneInfo:
    def __init__(self, name, offset, tz_id):
        self.name = name
        self.offset = str(offset)
        self.tz_id = tz_id

class TimeZoneService:
    def __init__(self, url):
        self.url = url
        self.time_zones = self._load_time_zones()

    def _load_time_zones(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            time_zones_data = json.loads(response.text)
            return [TimeZoneInfo(data['text'], data['offset'], data['value']) for data in time_zones_data]
        else:
            raise Exception(f"Failed to fetch time zone data. Status code: {response.status_code}")

    def filter_time_zones(self, match=None, offset=None):
        filtered_time_zones = self.time_zones

        if match:
            filtered_time_zones = [tz for tz in filtered_time_zones if match.lower() in tz.name.lower()]

        if offset:
            filtered_time_zones = [tz for tz in filtered_time_zones if str(offset) in tz.offset]

        return filtered_time_zones

    def display_time_zones(self, time_zones):
        table = [(tz.name, tz.offset, tz.tz_id) for tz in time_zones]
        print(tabulate.tabulate(table, headers=['Time Zone', 'Offset', 'ID']))

def main():
    parser = argparse.ArgumentParser(description="Display information about world time zones.")
    parser.add_argument("--match", help="Display time zones whose names match the specified string.")
    parser.add_argument("--offset", help="Display time zones matching the specified offset.")
    args = parser.parse_args()

    time_zone_service = TimeZoneService("https://raw.githubusercontent.com/dmfilipenko/timezones.json/master/timezones.json")
    filtered_time_zones = time_zone_service.filter_time_zones(args.match, args.offset)
    time_zone_service.display_time_zones(filtered_time_zones)

if __name__ == "__main__":
    main()
