from django.contrib import admin

from api.models import Dictionary, DictionaryVersion, DictionaryItem


class DictionaryVersionInline(admin.TabularInline):
    model = DictionaryVersion
    extra = 1


class DictionaryItemInline(admin.TabularInline):
    model = DictionaryItem
    extra = 1


@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'current_version', 'current_version_start_date', 'id')
    list_display_links = ('name', 'code')
    search_fields = ('code', 'name')
    inlines = [DictionaryVersionInline]

    def current_version(self, obj):
        version = obj.get_current_version()
        return version.version if version else "Нет текущей версии"

    def current_version_start_date(self, obj):
        version = obj.get_current_version()
        return version.start_date if version else "-"

    current_version.short_description = "Текущая версия"
    current_version_start_date.short_description = "Дата начала текущей версии"


@admin.register(DictionaryVersion)
class DictionaryVersionAdmin(admin.ModelAdmin):
    list_display = ('dictionary', 'dictionary_code', 'dictionary_name', 'version', 'start_date')
    list_display_links = ('dictionary', 'dictionary_code')
    search_fields = ('dictionary_code', 'version')
    inlines = [DictionaryItemInline]

    def dictionary_code(self, obj):
        return obj.dictionary.code

    def dictionary_name(self, obj):
        return obj.dictionary.name

    dictionary_code.short_description = "Код справочника"
    dictionary_name.short_description = "Наименование справочника"


@admin.register(DictionaryItem)
class DictionaryItemAdmin(admin.ModelAdmin):
    list_display = ('version', 'item_code', 'item_value')
    list_display_links = ('version', 'item_code')
    search_fields = ('version__version', 'item_code', 'item_value')
