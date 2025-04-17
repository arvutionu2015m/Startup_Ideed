from django.contrib import admin
from django.db.models import Count, Avg
from django.urls import path
from django.template.response import TemplateResponse
from django.utils.html import format_html
from .models import StartupIdea
from django.contrib.auth import get_user_model
from django.db.models.functions import Length

User = get_user_model()


@admin.register(StartupIdea)
class StartupIdeaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'short_description', 'created_at', 'has_original')
    readonly_fields = (
        'business_model',
        'value_proposition',
        'target_audience',
        'original_idea_link',
    )
    search_fields = ('description', 'business_model', 'value_proposition', 'target_audience')
    list_filter = ('created_at', 'user')

    fieldsets = (
        (None, {
            'fields': (
                'user',
                'description',
                'image',
                'business_model',
                'value_proposition',
                'target_audience',
                'original_idea_link',
            )
        }),
    )

    def short_description(self, obj):
        return obj.description[:40] + "..." if obj.description else "-"
    short_description.short_description = "Kirjeldus"

    def has_original(self, obj):
        return bool(obj.original_idea)
    has_original.boolean = True
    has_original.short_description = "Sarnane?"

    def original_idea_link(self, obj):
        if obj.original_idea and obj.original_idea.id:
            return format_html(
                '<a href="/admin/ideas/startupidea/{}/change/">Vaata ideed #{}</a>',
                obj.original_idea.id,
                obj.original_idea.id
            )
        return "-"
    original_idea_link.short_description = "Põhiidee viide"

    # --- STATISTIKA URL ---
    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path('statistics/', self.admin_site.admin_view(self.statistics_view), name='ideas_statistics'),
        ]
        return extra_urls + urls

    def statistics_view(self, request):
        total_ideas = StartupIdea.objects.count()
        ideas_per_user = User.objects.annotate(total=Count('startupidea')).order_by('-total')
        most_cloned = StartupIdea.objects.annotate(clones=Count('variants')).order_by('-clones')[:5]
        avg_desc = StartupIdea.objects.aggregate(avg=Avg(Length('description')))['avg']
        avg_val = StartupIdea.objects.aggregate(avg=Avg(Length('value_proposition')))['avg']

        context = dict(
            self.admin_site.each_context(request),
            total_ideas=total_ideas,
            ideas_per_user=ideas_per_user,
            most_cloned=most_cloned,
            avg_description_length=round(avg_desc or 0),
            avg_value_length=round(avg_val or 0),
        )
        return TemplateResponse(request, "admin/ideas/statistics.html", context)
