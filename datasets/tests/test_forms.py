import unittest
from ddt import ddt, data, unpack

from datasets.models import SchemaColumn
from datasets.forms import SchemaColumnForm


@ddt
class SchemaColumnFormTestCase(unittest.TestCase):
    @data(
        (SchemaColumn.DATE,),
        (SchemaColumn.FULLNAME,),
        (SchemaColumn.EMAIL,),
        (SchemaColumn.PHONE,),
        (SchemaColumn.COMPANY,),
        (SchemaColumn.JOB,),
        (SchemaColumn.DOMAIN,),
    )
    @unpack
    def test_valid_non_parametrized_form(self, field_type):
        form_data = {
            'order': 1,
            'name': 'test',
            'field_type': field_type,
        }
        form = SchemaColumnForm(data=form_data)
        self.assertTrue(form.is_valid())

    @data(
        (SchemaColumn.DATE, 0, 0, 0),
        (SchemaColumn.RANGED_INT, 10, 100, 0),
        (SchemaColumn.FULLNAME, 0, 0, 0),
        (SchemaColumn.EMAIL, 0, 0, 0),
        (SchemaColumn.TEXT, 0, 0, 5),
        (SchemaColumn.PHONE, 0, 0, 0),
        (SchemaColumn.COMPANY, 0, 0, 0),
        (SchemaColumn.JOB, 0, 0, 0),
        (SchemaColumn.DOMAIN, 0, 0, 0),
    )
    @unpack
    def test_valid_all_form(
            self, field_type, lower_bound, upper_bound, number_of_sentences
    ):
        form_data = {
            'order': 1,
            'name': 'test',
            'field_type': field_type,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'number_of_sentences': number_of_sentences,
        }
        form = SchemaColumnForm(data=form_data)
        self.assertTrue(form.is_valid())

    @data(
        (SchemaColumn.RANGED_INT,),
        (SchemaColumn.TEXT,),
    )
    @unpack
    def test_invalid_parametrized_form(self, field_type):
        form_data = {
            'order': 1,
            'name': 'test',
            'field_type': field_type,
        }
        form = SchemaColumnForm(data=form_data)
        self.assertFalse(form.is_valid())




