import unittest
import os
import tempfile
import sst

class SSTTestCase(unittest.TestCase):
    
    def test_validate_timecodes_bad_frames(self):
        with self.assertRaises(SystemExit) as cm:
            timestamp = ["0001", "01:00:16:27", "01:00:19:53", "image.bmp"]
            sst.validate_timecodes(timestamp)
        self.assertIn('Bad timestamp format-frames', cm.exception.args[0])

    def test_validate_timecodes_bad_seconds(self):
        with self.assertRaises(SystemExit) as cm:
            timestamp = ["0001", "01:00:16:27", "01:00:69:23", "image.bmp"]
            sst.validate_timecodes(timestamp)
        self.assertIn('Bad timestamp format-seconds', cm.exception.args[0])

    def test_validate_timecodes_bad_minutes(self):
        with self.assertRaises(SystemExit) as cm:
            timestamp = ["0001", "01:00:16:27", "01:60:19:23", "image.bmp"]
            sst.validate_timecodes(timestamp)
        self.assertIn('Bad timestamp format-minutes', cm.exception.args[0])

    def test_validate_timecodes_success(self):
        timestamp = ["0001", "01:00:16:27", "01:00:19:23", "image.bmp"]
        try:
            sst.validate_timecodes(timestamp)
        except:
            self.fail('Unexpected exception')

    def test_increment_line_frames(self):
        timestamp = ["0001", "01:00:16:27", "01:00:19:13", "image.bmp"]
        assert sst.increment_line(timestamp) == ["0001", "01:00:16:27", "01:00:19:14", "image.bmp"]

    def test_increment_line_seconds(self):
        timestamp = ["0001", "01:00:16:27", "01:00:19:29", "image.bmp"]
        assert sst.increment_line(timestamp) == ["0001", "01:00:16:27", "01:00:20:00", "image.bmp"]

    def test_increment_line_minutes(self):
        timestamp = ["0001", "01:00:16:27", "01:00:59:29", "image.bmp"]
        assert sst.increment_line(timestamp) == ["0001", "01:00:16:27", "01:01:00:00", "image.bmp"]

    def test_increment_line_hours(self):
        timestamp = ["0001", "01:00:16:27", "01:59:59:29", "image.bmp"]
        assert sst.increment_line(timestamp) == ["0001", "01:00:16:27", "02:00:00:00", "image.bmp"]

if __name__ == '__main__':
    unittest.main()

