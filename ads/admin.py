from django.contrib import admin

from ads.models import Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """ Админка для модели Ad. """

    list_display = ('id', 'user', 'title', 'category', 'condition', 'created_at',)
    list_filter = ("category", 'condition',)
    search_fields = ("name", "description",)
