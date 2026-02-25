import unittest

from modules.filename_utils import jd_number


class TestFilenameUtils(unittest.TestCase):
    def test_jd_number_variants(self):
        self.assertEqual(jd_number("jd1.pdf"), 1)
        self.assertEqual(jd_number("jd_1.pdf"), 1)
        self.assertEqual(jd_number("jd-12.pdf"), 12)
        self.assertEqual(jd_number("jd_2 (1).pdf"), 2)

    def test_jd_number_non_matching(self):
        self.assertIsNone(jd_number("random.pdf"))
        self.assertIsNone(jd_number("job_description.pdf"))


if __name__ == "__main__":
    unittest.main()
