from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import MagicMock, patch

from datasets.models import (
    Schema, DateColumnField, IntegerColumnField, EmailColumnField,
    FullNameColumnField, TextColumnField, PhoneColumnField, CompanyColumnField,
    JobColumnField, DomainNameColumnField
)


class SchemaTests(TestCase):
    global_schema = None
    author = None

    @classmethod
    def setUpTestData(cls) -> None:
        """Create instances before ALL tests of this TestCase"""
        cls.author = get_user_model().objects.create(
            username='test',
            password='test_pwd'
        )

        cls.global_schema = Schema.objects.create(
            name='global_schema',
            separator=Schema.SPACE,
            quote_type=Schema.SINGLE_QUOTE,
            author=cls.author
        )

        cls.name_field = cls.global_schema._meta.get_field('name')
        cls.separator_field = cls.global_schema._meta.get_field('separator')
        cls.quote_type_field = cls.global_schema._meta.get_field('quote_type')
        cls.author_field = cls.global_schema._meta.get_field('author')

    def setUp(self) -> None:
        """Create instances before EACH test"""
        self.local_schema = Schema.objects.create(
            name='local_schema',
            separator=Schema.SPACE,
            quote_type=Schema.SINGLE_QUOTE,
            author=self.author
        )

    # Testing verbose_name feature
    def test_name_field_verbose_name(self):
        real_verbose_name = getattr(self.name_field, 'verbose_name')
        expected_verbose_name = 'Schema name'
        self.assertEqual(real_verbose_name, expected_verbose_name)

    def test_separator_field_verbose_name(self):
        real_verbose_name = getattr(self.separator_field, 'verbose_name')
        expected_verbose_name = 'Schema separator'
        self.assertEqual(real_verbose_name, expected_verbose_name)

    def test_quote_type_field_verbose_name(self):
        real_verbose_name = getattr(self.quote_type_field, 'verbose_name')
        expected_verbose_name = 'Schema quote type'
        self.assertEqual(real_verbose_name, expected_verbose_name)

    # Testing max_length feature
    def test_name_field_max_length(self):
        real_max_length = getattr(self.name_field, 'max_length')
        self.assertEqual(real_max_length, 120)

    def test_separator_field_max_length(self):
        real_max_length = getattr(self.separator_field, 'max_length')
        self.assertEqual(real_max_length, 10)

    def test_quote_type_field_max_length(self):
        real_max_length = getattr(self.quote_type_field, 'max_length')
        self.assertEqual(real_max_length, 10)

    # Testing unique feature
    def test_name_field_unique(self):
        real_unique = getattr(self.name_field, 'unique')
        self.assertTrue(real_unique)

    def test_separator_field_unique(self):
        real_unique = getattr(self.separator_field, 'unique')
        self.assertFalse(real_unique)

    def test_quote_type_field_unique(self):
        real_unique = getattr(self.quote_type_field, 'unique')
        self.assertFalse(real_unique)

    def test_author_field_unique(self):
        real_unique = getattr(self.author_field, 'unique')
        self.assertFalse(real_unique)

    # Testing representation feature
    def test_str_method(self):
        self.assertEqual(str(self.global_schema), str(self.global_schema.name))
        self.assertEqual(str(self.local_schema), str(self.local_schema.name))

    # Testing model verbose_name feature
    def test_model_verbose_name(self):
        self.assertEqual(Schema._meta.verbose_name, 'Schema')

    # Testing model verbose_name_plural feature
    def test_model_verbose_name_plural(self):
        self.assertEqual(Schema._meta.verbose_name_plural, 'Schemes')

    def tearDown(self) -> None:
        """Delete instances after EACH test"""
        self.local_schema.delete()


class SchemaColumnTests(TestCase):
    mock = MagicMock()
    mock.__str__.return_value = ''

    @classmethod
    def setUpTestData(cls) -> None:
        """Create instances before ALL tests of this TestCase"""
        cls.author = get_user_model().objects.create(
            username='test',
            password='test_pwd'
        )

        cls.schema = Schema.objects.create(
            name='global_schema',
            separator=Schema.SPACE,
            quote_type=Schema.SINGLE_QUOTE,
            author=cls.author
        )

    @patch(
        "datasets.services.column_data_generator."
        "DateColumnDataGenerator.dump_date_value",
        return_value='2020-01-01'
    )
    def test_date_dump_data(self, mocked):
        column = DateColumnField.objects.create(
            order=1,
            name='Date',
            field_type=DateColumnField.RANGED_INT,
            schema=self.schema
        )
        self.assertEqual(column.generate_dump_value(), '2020-01-01')

    @patch(
        "datasets.services.column_data_generator."
        "IntColumnDataGenerator.dump_int_value",
        return_value=1
    )
    def test_int_dump_data(self, mocked):
        column = IntegerColumnField.objects.create(
            order=1,
            name='Integer',
            field_type=DateColumnField.DATE,
            lower_bound=0,
            upper_bound=10,
            schema=self.schema
        )
        self.assertEqual(column.generate_dump_value(), 1)

    @patch(
        "datasets.services.column_data_generator."
        "StringColumnDataGenerator.dump_str_value",
        return_value='sample'
    )
    def test_email_dump_data(self, mocked):
        column = EmailColumnField.objects.create(
            order=1,
            name='Email',
            field_type=DateColumnField.EMAIL,
            schema=self.schema
        )
        self.assertEqual(column.generate_dump_value(), 'sample@example.com')

    @patch(
        "datasets.services.column_data_generator."
        "StringColumnDataGenerator.dump_str_value",
        return_value='name'
    )
    def test_full_name_dump_data(self, mocked):
        column = FullNameColumnField.objects.create(
            order=1,
            name='Full name',
            field_type=DateColumnField.FULLNAME,
            schema=self.schema
        )
        self.assertEqual(column.generate_dump_value(), 'Name Name')

    @patch(
        "datasets.services.column_data_generator."
        "StringColumnDataGenerator.dump_str_value",
        return_value='some text bla-bla-bla'
    )
    def test_text_dump_data(self, mocked):
        column = TextColumnField.objects.create(
            order=1,
            name='Text',
            field_type=DateColumnField.TEXT,
            number_of_sentences=2,
            schema=self.schema
        )
        text_sample = "Some text bla-bla-bla. Some text bla-bla-bla."
        self.assertEqual(column.generate_dump_value(), text_sample)

    @patch(
        "datasets.services.column_data_generator."
        "PhoneColumnDataGenerator.dump_phone_value",
        return_value='1'
    )
    def test_phone_dump_data(self, mocked):
        column = PhoneColumnField.objects.create(
            order=1,
            name='Phone',
            field_type=DateColumnField.PHONE,
            schema=self.schema
        )
        self.assertEqual(column.generate_dump_value(), '1')

    @patch(
        "datasets.services.column_data_generator."
        "StringColumnDataGenerator.dump_str_value",
        return_value='Grizzly'
    )
    def test_company_dump_data(self, mocked):
        column = CompanyColumnField.objects.create(
            order=1,
            name='Company',
            field_type=DateColumnField.COMPANY,
            schema=self.schema
        )
        self.assertEqual(column.generate_dump_value(), 'Grizzly and co.')

    @patch(
        "datasets.services.column_data_generator."
        "JobColumnDataGenerator.dump_job_value",
        return_value='Middle Python dev'
    )
    def test_job_dump_data(self, mocked):
        column = JobColumnField.objects.create(
            order=1,
            name='Job',
            field_type=DateColumnField.JOB,
            schema=self.schema
        )
        self.assertEqual(column.generate_dump_value(), 'Middle Python dev')

    @patch(
        "datasets.services.column_data_generator."
        "StringColumnDataGenerator.dump_str_value",
        return_value='sample'
    )
    def test_domain_dump_data(self, mocked):
        column = DomainNameColumnField.objects.create(
            order=1,
            name='Domain',
            field_type=DateColumnField.DOMAIN,
            schema=self.schema
        )
        self.assertEqual(column.generate_dump_value(), 'sample.ua')



