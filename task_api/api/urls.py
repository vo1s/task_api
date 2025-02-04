from django.urls import path

from .views import RefbooksListAPIView, RefbookElementsAPIView, DictionaryElementValidationView

urlpatterns = [
    path('refbooks/', RefbooksListAPIView.as_view(), name='refbooks-list'),
    path('refbooks/<int:id>/elements', RefbookElementsAPIView.as_view(), name='refbook-elements'),
    path('refbooks/<int:id>/check_element', DictionaryElementValidationView.as_view(), name='dictionary-element-validation'),
]