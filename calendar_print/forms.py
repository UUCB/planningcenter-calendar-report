from django.forms import Form, DateInput
from django.utils import timezone
from datetime import timedelta
from django.forms.fields import DateField, BooleanField, CharField


class CalendarPrintForm(Form):
    start_date = DateField(widget=DateInput(attrs={'type': 'date'}), initial=timezone.now().date())
    end_date = DateField(widget=DateInput(attrs={'type': 'date'}), initial=timezone.now().date() + timedelta(days=7))
    header_text = CharField(required=False, initial="Events This Week")
    refresh = BooleanField(initial=True, required=False)