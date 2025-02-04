from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class Dictionary(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name="Код")
    name = models.CharField(max_length=300, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"

    def __str__(self):
        return self.name

    def get_current_version(self):
        return self.versions.filter(start_date__lte=now()).order_by('-start_date').first()


class DictionaryVersion(models.Model):
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name="versions",
                                   verbose_name="Справочник")
    version = models.CharField(max_length=50, verbose_name="Версия")
    start_date = models.DateField(verbose_name="Дата начала действия версии")

    class Meta:
        unique_together = ('dictionary', 'version')
        verbose_name = "Версия справочника"
        verbose_name_plural = "Версии справочников"

    def clean(self):
        if DictionaryVersion.objects.filter(dictionary=self.dictionary, start_date=self.start_date).exclude(
                pk=self.pk).exists():
            raise ValidationError("У одного справочника не может быть более одной версии с одинаковой датой начала.")

    def __str__(self):
        return f"{self.dictionary.code} - {self.version}"


class DictionaryItem(models.Model):
    version = models.ForeignKey(DictionaryVersion, on_delete=models.CASCADE, related_name="items",
                                verbose_name="Версия справочника")
    item_code = models.CharField(max_length=100, verbose_name="Код элемента")
    item_value = models.CharField(max_length=300, verbose_name="Значение элемента")

    class Meta:
        unique_together = ('version', 'item_code')
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочников"

    def __str__(self):
        return f"{self.item_code}: {self.item_value}"
