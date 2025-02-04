from django.utils.dateparse import parse_date
from django.utils.timezone import now
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Dictionary, DictionaryVersion, DictionaryItem


# Create your views here.

class BaseDictionaryAPIView(APIView):
    """
    Базовый класс для работы со справочниками.
    """

    def get_dictionary_version(self, dictionary, version=None):
        """
        Возвращает версию справочника по переданному version или текущую версию.
        """
        if not version:
            current_version = dictionary.get_current_version()
            if current_version is None:
                raise NotFound({"detail": "Нет доступных версий справочника."})
            version = current_version.version

        try:
            dictionary_version = DictionaryVersion.objects.get(dictionary=dictionary, version=version)
        except DictionaryVersion.DoesNotExist:
            raise NotFound({"detail": "Версия справочника не найдена."})

        return dictionary_version


class RefbooksListAPIView(APIView):
    """Получение списка справочников (+ актуальных на указанную дату)"""

    def get(self, request):
        date_param = request.GET.get("date")
        refbooks_query = Dictionary.objects.all()

        if date_param:
            try:
                date_obj = parse_date(date_param)
                if not date_obj:
                    raise ValueError
            except ValueError:
                return Response(
                    {"error": "Неверный формат даты. Используйте ГГГГ-ММ-ДД."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            refbooks_query = refbooks_query.filter(
                versions__start_date__lte=date_obj
            ).distinct()

        refbooks_data = [
            {"id": str(refbook.id), "code": refbook.code, "name": refbook.name}
            for refbook in refbooks_query
        ]

        return Response({"refbooks": refbooks_data}, status=status.HTTP_200_OK)


class RefbookElementsAPIView(BaseDictionaryAPIView):
    """Получение элементов заданного справочника"""

    def get(self, request, id):
        try:
            dictionary = Dictionary.objects.get(id=id)
        except Dictionary.DoesNotExist:
            raise NotFound("Справочник не найден.")

        version = request.GET.get('version')

        try:
            dictionary_version = self.get_dictionary_version(dictionary, version)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)

        # Получаем элементы для выбранной версии справочника
        curr_version_items = DictionaryItem.objects.filter(version=dictionary_version)

        refbooks_elements_data = [
            {"code": element.item_code, "value": element.item_value}
            for element in curr_version_items
        ]

        return Response({"elements": refbooks_elements_data}, status=status.HTTP_200_OK)


#
# В ТЗ не указано конкретная реализация ответа, поэтому предлагаю такой вариант
#
class DictionaryElementValidationView(BaseDictionaryAPIView):
    """Валидация элементов"""

    def get(self, request, id):
        try:
            dictionary = Dictionary.objects.get(id=id)
        except Dictionary.DoesNotExist:
            raise NotFound("Справочник не найден.")

        # Получаем параметры code и value
        code = request.GET.get('code')
        value = request.GET.get('value')

        if not code or not value:
            return Response(
                {"detail": "Необходимо передать параметры 'code' и 'value'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        version = request.GET.get('version')

        try:
            dictionary_version = self.get_dictionary_version(dictionary, version)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, существует ли элемент с данным кодом и значением в данной версии
        try:
            dictionary_item = DictionaryItem.objects.get(
                version=dictionary_version, item_code=code, item_value=value
            )
        except DictionaryItem.DoesNotExist:
            return Response(
                {"detail": "Элемент с таким кодом и значением не найден."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Если элемент найден
        return Response({"detail": "Элемент найден в справочнике."}, status=status.HTTP_200_OK)
