from django.db import models
from django.conf import settings

from datasets.services.column_data_generator import (
    IntColumnDataGenerator, StringColumnDataGenerator, JobColumnDataGenerator,
    PhoneColumnDataGenerator, DateColumnDataGenerator
)


class TimeStampModel(models.Model):
    """
    Abstract class for adding created and updated fields to our entities.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Schema(TimeStampModel):
    """
    General class for schemas for our datasets' generation.
    """
    # choices for selecting a separator for our schema
    COMMA = ','
    SEMICOLON = ';'
    TAB = '\t'
    SPACE = ' '
    PIPE = '|'
    SEPARATOR_CHOICES = [
        (COMMA, 'Comma (,)'),
        (SEMICOLON, 'Semicolon (;)'),
        (TAB, 'Tab (\\t)'),
        (SPACE, 'Space ( )'),
        (PIPE, 'Pipe (|)'),
    ]

    # choices for selecting string character
    SINGLE_QUOTE = '\''
    DOUBLE_QUOTE = '\"'
    QUOTE_CHOICES = [
        (SINGLE_QUOTE, 'Single quote (\')'),
        (DOUBLE_QUOTE, 'Double quote (\")'),
    ]

    name = models.CharField(max_length=120)
    separator = models.CharField(
        max_length=10,
        choices=SEPARATOR_CHOICES,
        default=COMMA,
    )
    quote_type = models.CharField(
        max_length=10,
        choices=QUOTE_CHOICES,
        default=SINGLE_QUOTE,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name

    @property
    def ordered_columns(self):
        """
        Return schema columns of this instance ordered by 'order' field.
        """
        return self.schemacolumn_set.order_by('order')

    @property
    def ordered_fields(self):
        """
        Return list of fields (Child classes for SchemaColumns)
        sorted by 'order' field
        """
        fields = get_field_from_column(self)
        fields.sort(key=lambda item: item.order)
        return fields

    def get_header(self) -> list:
        """
        Return list of names of schema columns.
        """
        return [item.name for item in self.ordered_columns]


class SchemaColumn(TimeStampModel):
    """
    General class for different schema column types.
    """
    # choices for selecting a field type for our column
    DATE = 'DATE'
    RANGED_INT = 'RANGED_INT'
    FULLNAME = 'FULLNAME'
    EMAIL = 'EMAIL'
    TEXT = 'TEXT'
    PHONE = 'PHONE'
    COMPANY = 'COMPANY'
    JOB = 'JOB'
    DOMAIN = 'DOMAIN'
    FIELD_TYPE_CHOICES = [
        (DATE, 'Date field'),
        (RANGED_INT, 'Ranged integer field'),
        (FULLNAME, 'Full name field'),
        (EMAIL, 'E-mail field'),
        (TEXT, 'Text field'),
        (PHONE, 'Phone field'),
        (COMPANY, 'Company field'),
        (JOB, 'Job field'),
        (DOMAIN, 'Domain name field'),
    ]

    order = models.IntegerField()
    name = models.CharField(max_length=30)
    field_type = models.CharField(
        max_length=10,
        choices=FIELD_TYPE_CHOICES,
        default=DATE,
    )
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.field_type} column: {self.name}'


class DateColumnField(SchemaColumn):
    """
    SchemaColumn with DATE field_type.
    """
    @staticmethod
    def generate_dump_value():
        gen = DateColumnDataGenerator()
        rand_date = gen.dump_date_value()
        return rand_date


class IntegerColumnField(SchemaColumn):
    """
    SchemaColumn with RANGED_INT field_type.
    """
    lower_bound = models.IntegerField()
    upper_bound = models.IntegerField()

    def __str__(self):
        return super().__str__() + f' ({self.lower_bound}-{self.upper_bound})'

    def generate_dump_value(self):
        gen = IntColumnDataGenerator(self.lower_bound, self.upper_bound)
        res = gen.dump_int_value()
        return res


class EmailColumnField(SchemaColumn):
    """
    SchemaColumn with EMAIL field_type.
    """
    @staticmethod
    def generate_dump_value():
        gen = StringColumnDataGenerator(6, 15)
        res = gen.dump_str_value()
        return f'{res}@example.com'


class FullNameColumnField(SchemaColumn):
    """
    SchemaColumn with FULLNAME field_type.
    """
    @staticmethod
    def generate_dump_value():
        gen = StringColumnDataGenerator(6, 15)
        name = gen.dump_str_value().capitalize()
        surname = gen.dump_str_value().capitalize()
        return f'{name} {surname}'


class TextColumnField(SchemaColumn):
    """
    SchemaColumn with TEXT field_type.
    """
    number_of_sentences = models.IntegerField()

    def generate_dump_value(self):
        gen = StringColumnDataGenerator(30, 150)
        sentences = []
        for _ in range(self.number_of_sentences):
            sentence = gen.dump_str_value().capitalize()
            sentences.append(sentence)
        res_text = '. '.join(sentences) + '.'
        return res_text


class PhoneColumnField(SchemaColumn):
    """
    SchemaColumn with PHONE field_type.
    """
    @staticmethod
    def generate_dump_value():
        gen = PhoneColumnDataGenerator()
        phone = gen.dump_phone_value()
        return phone


class CompanyColumnField(SchemaColumn):
    """
    SchemaColumn with COMPANY field_type.
    """

    @staticmethod
    def generate_dump_value():
        gen = StringColumnDataGenerator(6, 14)
        company_name = gen.dump_str_value().capitalize()
        return f'{company_name} and co.'


class JobColumnField(SchemaColumn):
    """
    SchemaColumn with JOB field_type.
    """
    @staticmethod
    def generate_dump_value():
        gen = JobColumnDataGenerator()
        job_name = gen.dump_job_value()
        return job_name


class DomainNameColumnField(SchemaColumn):
    """
    SchemaColumn with DOMAIN field_type.
    """
    @staticmethod
    def generate_dump_value():
        gen = StringColumnDataGenerator(6, 20)
        host_value = gen.dump_str_value()
        return f'{host_value}.ua'


class Dataset(TimeStampModel):
    """
    Model, which represent instance of dataset generated for particular schema.
    """
    PROCESSED = 'PROCESSED'
    READY = 'READY'
    STATUS_CHOICES = [
        (PROCESSED, 'Processed'),
        (READY, 'Ready'),
    ]

    file = models.FileField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PROCESSED
    )
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    def __str__(self):
        return f'Datasets on {self.schema} schema ({self.status})'


def get_field_from_column(schema):
    """
    Return list with subclasses for SchemaColumn of all field types
    (DateColumnField, IntegerColumnField etc.) from schema
    """
    field_classes_list = [
        DateColumnField, IntegerColumnField, FullNameColumnField,
        EmailColumnField, TextColumnField, PhoneColumnField,
        CompanyColumnField, JobColumnField, DomainNameColumnField,
    ]
    column_pk_list = [item.pk for item in schema.schemacolumn_set.all()]
    field_qss_list = []
    for field_class in field_classes_list:
        fields_qs = field_class.objects.filter(
            schemacolumn_ptr_id__in=column_pk_list
        )
        field_qss_list.append(fields_qs)

    from itertools import chain
    return list(chain(*field_qss_list))
