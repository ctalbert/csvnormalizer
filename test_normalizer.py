import unittest
import normalizer

class TestNormalizeTimestamp(unittest.TestCase):
    def test_invalid_string(self):
        invalid = '4/1/11 1�:00:00 AM'
        try:
            value = normalizer.normalize_timestamp(invalid)
            self.fail('Fail: did not throw')
        except ValueError:
            self.assertTrue(True, "Threw correct exception")
        
    
    def test_valid_strings(self):
        # usual string
        valid = '6/10/16 7:00:00 PM'
        value = normalizer.normalize_timestamp(valid)
        self.assertEqual(value, '2016-06-10T22:00:00-04:00')

        # slightly different, still ok
        valid = '6/10/16 7:00:00 pm'
        value = normalizer.normalize_timestamp(valid)
        self.assertEqual(value, '2016-06-10T22:00:00-04:00')

    @unittest.expectedFailure
    def test_euro_format(self):
        # This doesn't curerntly get handled
        euro = '22/10/99 10:00:00 am'
        try:
            normalizer.normalize_timestamp(euro)
        except ValueError:
            self.fail('Euro style dates not supported')

