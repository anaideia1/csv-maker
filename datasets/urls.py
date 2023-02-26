from django.urls import path
from . import views

app_name = 'datasets'
urlpatterns = [
    path('', views.SchemaListView.as_view(), name='schema-list'),
    path('create/', views.SchemaCreateView.as_view(), name='schema-create'),
    path('<int:pk>/detail/',
         views.SchemaDetailView.as_view(),
         name='schema-detail'),
    path('<int:pk>/edit/',
         views.SchemaUpdateView.as_view(),
         name='schema-edit'),
    path('<int:pk>/delete/',
         views.SchemaDeleteView.as_view(),
         name='schema-delete'),
]
