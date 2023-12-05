import django_tables2 as tables
from .models import InitiativeDetail

class QuestionsTable(tables.Table):
    edit = tables.TemplateColumn(
        template_name='edit.html',
        verbose_name='',
    )
    delete = tables.TemplateColumn(
        template_name='delete.html',
        verbose_name='',
    )
    selection = tables.CheckBoxColumn(accessor='pk', attrs={"th__input": {"onclick": 'toggle(this)'}}, orderable=False)
    tieback = tables.Column(verbose_name='Tie-back To Current State Findings')
    class Meta:
        model = InitiativeDetail
        template_name = "django_tables2/table.html"
        fields = ("initiative_id", "initiative", "description",  "tieback")