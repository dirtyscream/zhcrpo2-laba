from django.urls import path
from .views import DriveView

urlpatterns = [
    path('', DriveView.index, name='drive'),
    path('upload', DriveView.upload, name='upload'),
    path('<str:file_id>/delete', DriveView.delete, name='delete'),
    path('<str:file_id>/', DriveView.preview, name='preview')
]
