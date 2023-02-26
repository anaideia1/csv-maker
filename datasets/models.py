from django.db import models


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

    def __str__(self) -> str:
        return self.name

    @property
    def ordered_columns(self):
        """
        return schema columns of this instance ordered by 'order' field.
        """
        return self.schemacolumn_set.order_by('order')

    def get_header(self) -> list:
        """
        returns list of names of schema columns.
        """
        return [item.name for item in self.schemacolumn_set.all()]

    def get_types(self) -> list:
        """
        returns list of types of schema columns.
        """
        return [item.field_type for item in self.ordered_columns]


class SchemaColumn(TimeStampModel):
    """
    Representing class for different schema column types.
    """
    # choices for selecting a field type for our column
    DATE = 'DATE'
    RANGED_INT = 'RANGED_INT'
    FULLNAME = 'FULLNAME'
    EMAIL = 'EMAIL'
    TEXT = 'TEXT'
    FIELD_TYPE_CHOICES = [
        (DATE, 'Date field'),
        (RANGED_INT, 'Ranged integer field'),
        (FULLNAME, 'Full name field'),
        (EMAIL, 'E-mail field'),
        (TEXT, 'Text field'),
    ]

    order = models.IntegerField()
    name = models.CharField(max_length=30)
    field_type = models.CharField(
        max_length=10,
        choices=FIELD_TYPE_CHOICES,
        default=TEXT,
    )
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.field_type} column: {self.name}'


class IntegerRangeBound(TimeStampModel):
    """
    Class for lower and upper bound in RANGED_INT type for SchemaColumn.
    """
    lower_bound = models.IntegerField()
    upper_bound = models.IntegerField()
    schema_column = models.ForeignKey(SchemaColumn, on_delete=models.CASCADE)

    def __str__(self):
        return f'Between {self.lower_bound} and {self.upper_bound}'


class Dataset(TimeStampModel):
    """
    Model, which represent instance of data generated for particular schema.
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

