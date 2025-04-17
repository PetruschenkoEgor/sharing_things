from django.contrib import admin

from ads.models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Админка для модели Ad."""

    list_display = (
        "id",
        "user",
        "title",
        "category",
        "condition",
        "created_at",
    )
    list_filter = (
        "category",
        "condition",
    )
    search_fields = (
        "name",
        "description",
    )


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    """Админка для модели ExchangeProposal."""

    list_display = ("id", "owner", "comment", "status", "created_at")
