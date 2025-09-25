from django.urls import path

from calendar_print.views import CalendarPrintView

urlpatterns = [
    path('', CalendarPrintView.as_view(), name='calendar-print'),
]