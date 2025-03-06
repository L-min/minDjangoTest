from django.contrib import admin
from django.contrib.admin.utils import quote
from django.contrib.admin.templatetags import admin_list
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
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
    list_display = [
        "question_text",
        "pub_date",
        "was_published_recently",
    ]
    list_filter = ["pub_date"]
    list_display_links = ["pub_date"]
    list_editable = ["question_text"]

    search_fields = ["question_text"]
    actions = ["change_question_text"]

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
            ),
        ]
        return my_urls + urls

    @admin.action(description="question_textをotherに変更")
    def change_question_text(modeladmin, request, queryset):
        queryset.update(question_text="other")


class CustomQuestion(Question):
    class Meta:
        proxy = True


class CustomQuestionAdmin(QuestionAdmin):
    actions = ["change_question_text", "make_published"]
    list_display = [
        "question_text",
        "detail_button",
        "pub_date",
        "was_published_recently",
    ]
    list_display_links = ["detail_button", "pub_date"]

    @admin.action(description="現在時刻で公開")
    def make_published(modeladmin, request, queryset):
        now = timezone.now()

        queryset.update(pub_date=now)

    # カスタム一覧ページ
    def changelist_view(self, request, extra_context=None):
        app_label = self.opts.app_label

        templateResponse = super().changelist_view(request, extra_context)
        templateResponse.template_name = [
            "admin/%s/%s/change_list_custom.html" % (app_label, self.opts.model_name),
            "admin/%s/change_list_custom.html" % app_label,
            "admin/change_list_custom.html",
        ]
        templateResponse.context = extra_context

        return templateResponse

    # 行に編集ボタン追加
    def detail_button(self, obj):
        buttonClasses = ["button", "default"]
        row_class = mark_safe(' class="%s"' % " ".join(buttonClasses))

        return format_html(
            "<button {} type={} style='padding: 5px 10px;'>{}</button>",
            row_class,
            "button",
            "編集する",
        )


admin.site.register(Question, QuestionAdmin)
admin.site.register(CustomQuestion, CustomQuestionAdmin)
