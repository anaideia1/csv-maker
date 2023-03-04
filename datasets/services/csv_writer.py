import csv
import os
from django.core.files.base import File
from django.conf import settings

from datasets.models import Schema, Dataset


class CsvGenerator:
    """
    Class for creating dataset and generating dump data file.
    """
    def __init__(self, schema_: Schema, num_rows_: int) -> None:
        super(CsvGenerator, self).__init__()
        self.schema = schema_
        self.num_rows = num_rows_

    @classmethod
    def _generate_row(cls, fields) -> list:
        """
        Method for generating one row of values via fields.
        Fields its ordered list of child classes for SchemaColumn,
        as DateColumnField, FullNameColumnField etc.
        """
        return [field.generate_dump_value() for field in fields]

    def _data_generator(self):
        """
        Generator-func for generator with dump data for specific number of rows
        """
        fields = self.schema.ordered_fields
        for i in range(self.num_rows):
            yield self._generate_row(fields)

    def _generate_dump_file(self, file_name: str, dataset: Dataset) -> None:
        """
        Function for creating and filling file with dump data.
        """
        file_path = os.path.join(settings.MEDIA_ROOT, 'temp_data_file.csv')
        with open(file_path, 'w+', encoding='UTF8', newline='') as f:
            file = File(f)
            writer = csv.writer(
                file,
                delimiter=self.schema.separator,
                quotechar=self.schema.quote_type
            )
            header = self.schema.get_header()
            writer.writerow(header)

            for row in self._data_generator():
                writer.writerow(row)

            import time
            time.sleep(2)

            dataset.file.save(file_name, file)
            dataset.status = Dataset.READY

        os.remove(file_path)

    def generate_dataset(self) -> Dataset:
        """
        General function for creating file and filling it with dump data.
        Also creating dataset and attaching it to our generated file.
        """
        dataset = Dataset.objects.create(
            status=Dataset.PROCESSED,
            schema=self.schema
        )
        file_name = f'{self.schema.name}_{dataset.created_at}.csv'
        self._generate_dump_file(file_name, dataset)
        dataset.save()

        return dataset
