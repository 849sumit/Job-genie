import unittest

from job_genie_backend import greet


class TestJobGenieBackend(unittest.TestCase):
    def test_greet_default(self):
        self.assertEqual(greet(), "Hello, World! Welcome to Job Genie Backend.")

    def test_greet_name(self):
        self.assertEqual(greet("Alice"), "Hello, Alice! Welcome to Job Genie Backend.")


if __name__ == "__main__":
    unittest.main()
