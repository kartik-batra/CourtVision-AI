from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('',                    views.notes_list,       name='notes'),
    path('create/',             views.note_create,      name='create'),
    path('<int:pk>/',           views.note_detail,      name='detail'),
    path('<int:pk>/edit/',      views.note_edit,        name='edit'),
    path('<int:pk>/delete/',    views.note_delete,      name='delete'),
    path('<int:pk>/pin/',       views.note_toggle_pin,  name='toggle_pin'),
    path('quick/',              views.note_quick_save,  name='quick_save'),
]
