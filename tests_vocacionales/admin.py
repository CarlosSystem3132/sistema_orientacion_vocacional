from django.contrib import admin
from .models import Pregunta, Opcion, Respuesta, AreaVocacional, ResultadoTest

class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 5

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'tipo_test', 'get_area_vocacional')
    list_filter = ('tipo_test', 'area_vocacional')
    search_fields = ('texto',)
    inlines = [OpcionInline]

    def get_area_vocacional(self, obj):
        return obj.area_vocacional.nombre
    get_area_vocacional.short_description = 'Área Vocacional'

@admin.register(AreaVocacional)
class AreaVocacionalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'pregunta', 'opcion')
    list_filter = ('usuario', 'pregunta__tipo_test')

@admin.register(ResultadoTest)
class ResultadoTestAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'area_vocacional', 'puntaje', 'fecha')
    list_filter = ('usuario', 'area_vocacional')
    date_hierarchy = 'fecha'

