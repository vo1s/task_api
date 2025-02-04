from django.urls import reverse
from rest_framework.test import APITestCase
from api.models import Dictionary, DictionaryVersion, DictionaryItem
from django.utils import timezone


class RefbooksListAPIViewTests(APITestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.dictionary1 = Dictionary.objects.create(code="ref1", name="Reference Book 1")
        self.dictionary2 = Dictionary.objects.create(code="ref2", name="Reference Book 2")

        # Создаем версии для справочников
        self.version1 = DictionaryVersion.objects.create(dictionary=self.dictionary1, version="1.0",
                                                         start_date=timezone.now())
        self.version2 = DictionaryVersion.objects.create(dictionary=self.dictionary2, version="1.0",
                                                         start_date=timezone.now())

    def test_get_refbooks_without_date(self):
        url = reverse('refbooks-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['refbooks']), 2)

    def test_get_refbooks_with_valid_date(self):
        url = reverse('refbooks-list')
        response = self.client.get(url, {'date': '2025-10-01'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['refbooks']), 2)

    def test_get_refbooks_with_invalid_date(self):
        url = reverse('refbooks-list')
        response = self.client.get(url, {'date': 'invalid-date'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "Неверный формат даты. Используйте ГГГГ-ММ-ДД.")

class RefbookElementsAPIViewTests(APITestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.dictionary = Dictionary.objects.create(code="ref1", name="Reference Book 1")
        self.version = DictionaryVersion.objects.create(dictionary=self.dictionary, version="1.0", start_date=timezone.now())
        self.item1 = DictionaryItem.objects.create(version=self.version, item_code="code1", item_value="value1")
        self.item2 = DictionaryItem.objects.create(version=self.version, item_code="code2", item_value="value2")

    def test_get_elements_without_version(self):
        url = reverse('refbook-elements', args=[self.dictionary.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['elements']), 2)

    def test_get_elements_with_version(self):
        url = reverse('refbook-elements', args=[self.dictionary.id])
        response = self.client.get(url, {'version': '1.0'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['elements']), 2)

    def test_get_elements_with_invalid_version(self):
        url = reverse('refbook-elements', args=[self.dictionary.id])
        response = self.client.get(url, {'version': '2.0'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], "Версия справочника не найдена.")

    def test_get_elements_for_nonexistent_dictionary(self):
        url = reverse('refbook-elements', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], "Справочник не найден.")

class DictionaryElementValidationViewTests(APITestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.dictionary = Dictionary.objects.create(code="ref1", name="Reference Book 1")
        self.version = DictionaryVersion.objects.create(dictionary=self.dictionary, version="1.0", start_date=timezone.now())
        self.item = DictionaryItem.objects.create(version=self.version, item_code="code1", item_value="value1")

    def test_validate_element_with_valid_code_and_value(self):
        url = reverse('dictionary-element-validation', args=[self.dictionary.id])
        response = self.client.get(url, {'code': 'code1', 'value': 'value1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], "Элемент найден в справочнике.")

    def test_validate_element_with_invalid_code_or_value(self):
        url = reverse('dictionary-element-validation', args=[self.dictionary.id])
        response = self.client.get(url, {'code': 'code1', 'value': 'wrong_value'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], "Элемент с таким кодом и значением не найден.")

    def test_validate_element_without_code_or_value(self):
        url = reverse('dictionary-element-validation', args=[self.dictionary.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], "Необходимо передать параметры 'code' и 'value'.")

    def test_validate_element_with_invalid_version(self):
        url = reverse('dictionary-element-validation', args=[self.dictionary.id])
        response = self.client.get(url, {'code': 'code1', 'value': 'value1', 'version': '2.0'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], "Версия справочника не найдена.")

    def test_validate_element_for_nonexistent_dictionary(self):
        url = reverse('dictionary-element-validation', args=[999])
        response = self.client.get(url, {'code': 'code1', 'value': 'value1'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], "Справочник не найден.")