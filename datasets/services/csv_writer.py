import csv
import datetime
from django.core.files.base import File
from django.conf import settings

from datasets.models import Schema, SchemaColumn, Dataset


class CsvGenerator:
    def __init__(self, schema_: Schema, num_rows_: int):
        super(CsvGenerator, self).__init__()
        self.schema = schema_
        self.num_rows = num_rows_

    @staticmethod
    def _generate_value(field_type):
        if field_type == SchemaColumn.DATE:
            res = datetime.datetime.today()
        elif field_type == SchemaColumn.RANGED_INT:
            res = 20
        elif field_type == SchemaColumn.FULLNAME:
            res = 'asd asd'
        elif field_type == SchemaColumn.EMAIL:
            res = 'asd@sad.com'
        elif field_type == SchemaColumn.TEXT:
            res = 'asd'
        else:
            res = None

        return res

    @classmethod
    def _generate_row(cls, field_types):
        return list(map(cls._generate_value, field_types))

    def _data_generator(self):
        field_types = self.schema.get_types()
        for i in range(self.num_rows):
            yield self._generate_row(field_types)

    def _generate_dump_file(self, file_name):
        with open(f'{file_name}', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(
                f,
                delimiter=self.schema.separator,
                quotechar=self.schema.quote_type
            )
            header = self.schema.get_header()
            writer.writerow(header)

            for row in self._data_generator():
                writer.writerow(row)

            import time
            time.sleep(2)

    def generate_dataset(self):
        dataset = Dataset.objects.create(
            status=Dataset.PROCESSED,
            schema=self.schema
        )

        file_name = f'media/{self.schema.name}_{dataset.created_at}.csv'
        self._generate_dump_file(file_name)

        with open(f'{file_name}') as file:
            dataset.file = File(file)
            dataset.status = Dataset.READY
            dataset.save()

        return dataset
