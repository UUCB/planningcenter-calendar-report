from django.forms import Form
from django.forms.fields import DateField

class CalendarPrintForm(Form):
    start_date = DateField()
    end_date = DateField()