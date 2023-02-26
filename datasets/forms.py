from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, BaseInlineFormSet

from datasets.models import Schema, SchemaColumn


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'separator': forms.Select(attrs={'class': 'form-control'}),
            'quote_type': forms.Select(attrs={'class': 'form-control'}),
        }


class SchemaColumnForm(forms.ModelForm):
    DELETE = 'DELETE'

    class Meta:
        model = SchemaColumn
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', }),
            'field_type': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item in self.fields.values():
            item.required = False

    def clean(self):
        cleaned_data = super(SchemaColumnForm, self).clean()
        if self._is_empty_form(cleaned_data):
            cleaned_data[self.DELETE] = True
        elif not self._is_full_form(cleaned_data):
            errors = self._get_required_fields_errors(cleaned_data)
            raise ValidationError(errors)
        return cleaned_data

    @staticmethod
    def _is_empty_form(data):
        data.pop('schema')
        return not any(item for item in data.values())

    @staticmethod
    def _is_full_form(data):
        return all(item for item in data.values())

    @classmethod
    def _get_required_fields_errors(cls, data):
        res = {}
        for name, value in data.items():
            if not value and name not in ['id', cls.DELETE]:
                res.update({name: 'This field is required'})
        return res


class BaseSchemaColumnFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        """ hide deletion fields """
        super().add_fields(form, index)
        if 'DELETE' in form.fields:
            form.fields['DELETE'].widget = forms.HiddenInput()

    def clean(self):
        """ validate names and order through all forms in formset """
        super(BaseSchemaColumnFormSet, self).clean()
        if any(self.errors):
            return
        orders = []
        names = []
        if not any(not self._should_delete_form(form) for form in self.forms):
            raise forms.ValidationError(
                'Should be at least one column in schema'
            )
        for form in self.forms:
            if self._should_delete_form(form):
                continue
            order = form.cleaned_data.get('order')
            name = form.cleaned_data.get('name')
            if order in orders:
                raise forms.ValidationError(
                    'Orders in one schema must have distinct values'
                )
            else:
                orders.append(order)

            if name in names:
                raise forms.ValidationError(
                    'Names in one schema must be different'
                )
            else:
                names.append(name)


SchemaColumnFormSet = inlineformset_factory(
    Schema, SchemaColumn, form=SchemaColumnForm, exclude=('delete', ),
    formset=BaseSchemaColumnFormSet, min_num=1, extra=0
)


class DatasetGeneratorForm(forms.Form):
    num_rows = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super(DatasetGeneratorForm, self).clean()

        if not cleaned_data.get('num_rows'):
            raise forms.ValidationError("Enter number of rows.")

        return cleaned_data
