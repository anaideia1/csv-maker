import unittest
import datetime
from datasets.services.column_data_generator import (
    IntColumnDataGenerator, StringColumnDataGenerator, DateColumnDataGenerator,
    JobColumnDataGenerator, PhoneColumnDataGenerator
)


class TestColumnDataGenerator(unittest.TestCase):
    NUMBER_OF_TRIES = 100

    def test_int_data_generator(self):
        bounds = [
            (-100, -10),
            (-100, 100),
            (10, 100),
        ]

        for lower_bound, upper_bound in bounds:
            int_generator = IntColumnDataGenerator(lower_bound, upper_bound)

            generated_data = [
                int_generator.dump_int_value()
                for _ in range(self.NUMBER_OF_TRIES)
            ]

            for item in generated_data:
                self.assertIsInstance(item, int)
                self.assertGreaterEqual(item, lower_bound)
                self.assertLessEqual(item, upper_bound)

    def test_string_data_generator(self):
        min_length = 5
        max_length = 50
        str_generator = StringColumnDataGenerator(min_length, max_length)

        generated_data = [
            str_generator.dump_str_value()
            for _ in range(self.NUMBER_OF_TRIES)
        ]

        for item in generated_data:
            self.assertIsInstance(item, str)
            self.assertGreaterEqual(len(item), min_length)
            self.assertLessEqual(len(item), max_length)

    def test_job_data_generator(self):
        job_generator = JobColumnDataGenerator()

        generated_data = [
            job_generator.dump_job_value()
            for _ in range(self.NUMBER_OF_TRIES)
        ]

        for item in generated_data:
            self.assertIsInstance(item, str)
            parts = item.split(' ')
            self.assertGreaterEqual(len(parts), 3)
            self.assertIn(parts[0], job_generator.LEVEL_CHOICES)
            self.assertIn(parts[1], job_generator.LANGUAGE_CHOICES)
            self.assertEqual(parts[2], 'developer')

    def test_date_data_generator(self):
        date_generator = DateColumnDataGenerator()

        generated_data = [
            date_generator.dump_date_value()
            for _ in range(self.NUMBER_OF_TRIES)
        ]

        for item in generated_data:
            self.assertIsInstance(item, datetime.datetime)

    def test_phone_data_generator(self):
        phone_generator = PhoneColumnDataGenerator()

        generated_data = [
            phone_generator.dump_phone_value()
            for _ in range(self.NUMBER_OF_TRIES)
        ]

        for item in generated_data:
            self.assertIsInstance(item, str)
            self.assertEqual(len(item), 13)
            self.assertEqual(item[:4], '+380')
            self.assertTrue(item[1:].isdigit())
