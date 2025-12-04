from django.urls import path
from .views import PasteView

urlpatterns = [
    path('create/', PasteView.index, name='pin_create'),
    path('<slug:pin_id>/', PasteView.preview, name='pin_preview'),
    path('<slug:pin_id>/download', PasteView.download, name='pin_download'),
    path('<slug:pin_id>/delete', PasteView.delete, name='pin_delete')
]