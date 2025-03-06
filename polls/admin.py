from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse

from .models import Choice, Question
from . import views


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

    # 編集ページ修正
    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra = extra_context or {}
        extra["title"] = "questionを編集"

        return super(QuestionAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra
        )

    # ページ追加
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "new_page/",
                self.admin_site.admin_view(views.NewPageView.as_view()),
                name="new-page",
            )
        ]
        return my_urls + urls


admin.site.register(Question, QuestionAdmin)
