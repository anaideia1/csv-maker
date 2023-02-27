from django.contrib import admin

from .models import (
    Schema, SchemaColumn, Dataset, IntegerColumnField, TextColumnField,
    EmailColumnField, DateColumnField, FullNameColumnField
)


admin.site.register(Schema)
admin.site.register(SchemaColumn)
admin.site.register(Dataset)
admin.site.register(IntegerColumnField)
admin.site.register(TextColumnField)
admin.site.register(EmailColumnField)
admin.site.register(DateColumnField)
admin.site.register(FullNameColumnField)
