from django.urls import path
from . import views

app_name = 'research'

urlpatterns = [
    path('document/<int:pk>/',           views.research_interface, name='interface'),
    path('document/<int:pk>/query/',     views.submit_query,       name='query'),
    path('query/<int:query_id>/',        views.query_detail,       name='query_detail'),
    path('query/<int:query_id>/delete/', views.delete_query,       name='delete_query'),
    path('history/',                     views.research_history,   name='history'),
    path('query/<int:query_id>/translate/', views.translate_query_response, name='translate_query'),
]
