from django.test import TestCase
from django.contrib.auth import get_user_model

from datasets.models import Schema


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
