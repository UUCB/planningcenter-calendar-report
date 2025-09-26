import datetime

import pypco
from django.conf import settings
from calendar_print.models import Event
from django.utils import timezone
from django.utils.dateparse import parse_datetime


def get_pco():
    pco = pypco.PCO(
        settings.PLANNING_CENTER_APPLICATION_ID,
        settings.PLANNING_CENTER_SECRET,
    )
    return pco


def get_events(until) -> list:
    pco = get_pco()
    output_events = []
    upcoming_event_instances = pco.iterate(
        '/calendar/v2/event_instances',
        order='starts_at',
        include='event',
        filter='future',
    )
    for event_instance in upcoming_event_instances:
        if event_instance['data']['attributes']['all_day_event']:
            continue  # Ignore all day events for now, as we currently have no good way to display them
        if not event_instance['data']['attributes']['published_starts_at']:
            continue  # Ignore anything that doesn't have a start time; these events will break things
        if parse_datetime(event_instance['data']['attributes']['published_starts_at']).date() > until:
            break  # Break out of the loop if we have enough events
        event = pco.get(
            event_instance['data']['relationships']['event']['links']['related']
        )
        if event['data']['attributes']['visible_in_church_center']\
                and event_instance['data']['attributes']['published_starts_at']\
                and event_instance['data']['attributes']['published_ends_at']:
            output_events.append(Event(
                planning_center_instance_id=event_instance['data']['id'],
                planning_center_event_id=event['data']['id'],
                name=event['data']['attributes']['name'],
                start_time=timezone.localtime(
                    parse_datetime(
                        event_instance['data']['attributes']['published_starts_at']
                    )
                ),
                end_time=timezone.localtime(
                    parse_datetime(
                        event_instance['data']['attributes']['published_ends_at']
                    )
                ),
                date=timezone.localtime(
                    parse_datetime(
                        event_instance['data']['attributes']['published_starts_at']
                    )
                ).date(),
                link=f'https://uucb.churchcenter.com/calendar/event/{event_instance['data']["id"]}',
                description=event['data']['attributes']['description'],
                # Add the other fields
                # Write the actual update function like we have in voting system
            ))
    return output_events


def update_events(events: list) -> None:
    for event in Event.objects.all():
        event.just_imported = False
        event.save()
    for new_event in events:
        try:
            event_object = Event.objects.get(planning_center_instance_id=new_event.planning_center_instance_id)
        except Event.DoesNotExist:
            event_object = Event(planning_center_instance_id=new_event.planning_center_instance_id)
        event_object.just_imported = True
        event_object.planning_center_event_id = new_event.planning_center_event_id
        event_object.name = new_event.name
        event_object.start_time = new_event.start_time
        event_object.end_time = new_event.end_time
        event_object.link = new_event.link
        event_object.description = new_event.description
        event_object.date = new_event.date
        event_object.save()
    for event in Event.objects.filter(just_imported=False):
        event.delete()
