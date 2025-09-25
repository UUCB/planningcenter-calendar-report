from django.shortcuts import render
from django.views.generic import FormView

from calendar_print.forms import CalendarPrintForm
from calendar_print.models import Event
from planningcenter_calendar_report import planningcenter_extras

class CalendarPrintView(FormView):
    template_name = 'calendar_print/options.html'
    form_class = CalendarPrintForm

    def form_valid(self, form):
        print('VALID')
        planningcenter_extras.update_events(planningcenter_extras.get_events(until=form.cleaned_data['end_date']))
        return render(
            self.request,
            'calendar_print/report.html',
            {
                'events': Event.objects.filter(start_time__gte=form.cleaned_data['start_date'], start_time__lte=form.cleaned_data['end_date']),
            }
        )

