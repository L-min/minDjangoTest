from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra = extra_context or {}
        extra['title'] = 'questionを編集'

        return super(QuestionAdmin, self).change_view(request, object_id, form_url, extra_context=extra)

admin.site.register(Question, QuestionAdmin)