import unittest
from unittest.mock import patch
from io import StringIO
from my_timezone_program import TimeZoneService, TimeZoneInfo

class TestTimeZoneService(unittest.TestCase):
    def setUp(self):
        self.time_zone_service = TimeZoneService("https://raw.githubusercontent.com/dmfilipenko/timezones.json/master/timezones.json")

    @patch('builtins.input', side_effect=[''])
    def test_display_time_zones_no_filter(self, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.time_zone_service.display_time_zones(self.time_zone_service.time_zones)

        result = mock_stdout.getvalue().strip()
        self.assertIn("Time Zone", result)
        self.assertIn("Offset", result)
        self.assertIn("ID", result)

    @patch('builtins.input', side_effect=['Europe'])
    def test_filter_time_zones_by_match(self, mock_input):
        filtered_time_zones = self.time_zone_service.filter_time_zones(match="Europe")
        self.assertTrue(all("Europe" in tz.name for tz in filtered_time_zones))

    @patch('builtins.input', side_effect=['-07:00'])
    def test_filter_time_zones_by_offset(self, mock_input):
        filtered_time_zones = self.time_zone_service.filter_time_zones(offset="-07:00")
        self.assertTrue(all("-07:00" in tz.offset for tz in filtered_time_zones))

if __name__ == '__main__':
    unittest.main()
