from django.shortcuts import render
from django.views.generic import FormView

from calendar_print.forms import CalendarPrintForm
from calendar_print.models import Event
from planningcenter_calendar_report import planningcenter_extras

from datetime import datetime, date, timedelta

def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)


class DayWithEvents():
    def __init__(self, my_date):
        self.date = my_date

    def events(self):
        return Event.objects.filter(date=self.date)

class CalendarPrintView(FormView):
    template_name = 'calendar_print/options.html'
    form_class = CalendarPrintForm

    def form_valid(self, form):
        if form.cleaned_data['refresh']:
            planningcenter_extras.update_events(planningcenter_extras.get_events(until=form.cleaned_data['end_date']))
        return render(
            self.request,
            'calendar_print/report.html',
            {
                'page_per_day': form.cleaned_data['page_per_day'],
                'header_text': form.cleaned_data['header_text'],
                'days': [
                    DayWithEvents(day)
                    for day in daterange(
                        form.cleaned_data['start_date'],
                        form.cleaned_data['end_date'] + timedelta(days=1)  # make the end of the range inclusive
                    )
                ],
            }
        )

