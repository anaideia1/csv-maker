from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from datasets.forms import (
    SchemaForm, SchemaColumn, SchemaColumnFormSet, DatasetGeneratorForm,
    IntegerRangeBound,
)
from datasets.models import Schema
from datasets.services.csv_writer import CsvGenerator


class SchemaListView(LoginRequiredMixin, generic.ListView):
    """
    ListView for Schema model.
    """
    model = Schema


class SchemaCreateOrUpdateView(LoginRequiredMixin):
    """
    Class for common functionality for create and updated views.
    """
    form_class = SchemaForm
    model = Schema
    template_name = 'datasets/schema_create_form.html'
    object = None
    success_url = reverse_lazy('datasets:schema-list')

    @staticmethod
    def _is_formset_valid(schema_columns):
        is_every_form_valid = all(x.is_valid() for x in schema_columns)
        is_whole_form_valid = schema_columns.is_valid()
        return is_every_form_valid and is_whole_form_valid

    def _form_objects_saving(self, form, schema_columns):
        with transaction.atomic():
            self.object = form.save()
            columns = schema_columns.save(commit=False)
            for item, _ in schema_columns.deleted_objects:
                item.delete()

            for column, data in columns:
                column.schema = self.object
                column.save()
                if column.field_type == SchemaColumn.RANGED_INT:
                    IntegerRangeBound.objects.create(
                        lower_bound=data.get('lower_bound'),
                        upper_bound=data.get('upper_bound'),
                        schema_column=column,
                    )


class SchemaCreateView(SchemaCreateOrUpdateView, generic.CreateView):
    """
    CreateView for Schema model (as well for Schema Columns via formsets).
    """
    def get_context_data(self, **kwargs):
        data = super(SchemaCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['schema_columns'] = SchemaColumnFormSet(
                self.request.POST or None
            )
        else:
            data['schema_columns'] = SchemaColumnFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        schema_columns = context['schema_columns']

        if not self._is_formset_valid(schema_columns):
            return self.render_to_response(self.get_context_data(form=form))

        self._form_objects_saving(form, schema_columns)
        return redirect('datasets:schema-list')


class SchemaUpdateView(SchemaCreateOrUpdateView, generic.UpdateView):
    """
    UpdateView for Schema model (as well for Schema Columns via formsets).
    """
    def get_context_data(self, **kwargs):
        data = super(SchemaUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['schema_columns'] = SchemaColumnFormSet(
                self.request.POST or None, instance=self.object
            )
        else:
            data['schema_columns'] = SchemaColumnFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        schema_columns = context['schema_columns']

        if not self._is_formset_valid(schema_columns):
            return self.render_to_response(self.get_context_data(form=form))
        else:
            self._form_objects_saving(form, schema_columns)
            return redirect('datasets:schema-list')


class SchemaDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    DeleteView for Schema model.
    """
    model = Schema
    success_url = reverse_lazy('datasets:schema-list')


class SchemaDetailView(LoginRequiredMixin, View):
    """
    DetailView for Schema model. Also implement csv-generator functionality.
    """
    form_class = DatasetGeneratorForm
    template_name = 'datasets/schema_detail.html'

    def get(self, *args, **kwargs):
        form = self.form_class()
        schema_pk = self.kwargs['pk']
        schema = get_object_or_404(
            Schema.objects.prefetch_related('schemacolumn_set'), pk=schema_pk
        )
        return render(self.request, self.template_name,
                      {"form": form, "schema": schema})

    def post(self, *args, **kwargs):
        request = self.request
        is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        if is_ajax and request.method == "POST":
            form = self.form_class(self.request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                schema_pk = self.kwargs['pk']
                schema = get_object_or_404(Schema, pk=schema_pk)
                csv_generator = CsvGenerator(schema, form_data.get('num_rows'))
                dataset = csv_generator.generate_dataset()
                ser_instance = serializers.serialize('json', [dataset, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)

        return JsonResponse({"error": ""}, status=400)
