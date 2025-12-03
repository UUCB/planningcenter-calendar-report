from django.forms import Form, DateInput
from django.utils import timezone
from datetime import timedelta
from django.forms.fields import DateField, BooleanField, CharField

def get_sunday():
    sunday = timezone.now().date() + timedelta(days=6 - timezone.now().weekday() % 7)
    return sunday

def get_following_sunday():
    return get_sunday() + timedelta(days=7)

class CalendarPrintForm(Form):
    start_date = DateField(widget=DateInput(attrs={'type': 'date'}), initial=get_sunday)
    end_date = DateField(widget=DateInput(attrs={'type': 'date'}), initial=get_following_sunday)
    header_text = CharField(required=False, initial="Events This Week")
    page_per_day = BooleanField(initial=False, required=False)
    refresh = BooleanField(initial=True, required=False)