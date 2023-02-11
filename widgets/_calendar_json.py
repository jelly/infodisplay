'''
Json Calendar Widget

Uses a `jsonCalendar` file

'''

import logging
import json
from datetime import datetime, timedelta, timezone


wName = 'Calendar'


class JsonCalendar:

    def __init__(self, cfg):
        self.name = __name__
        self.logger = logging.getLogger(self.name)
        self.calendar_file = cfg.get(wName, 'jsonFile', fallback="")

    def get_calendar_items(self, dt, days_ahead):
        # Get start and end times in UTC
        utc_time = dt.astimezone(timezone.utc)
        time_ahead = dt + timedelta(days=days_ahead)
        time_ahead = time_ahead.replace(hour=23, minute=59, second=59, microsecond=0)

        events = []
        self.logger.debug('reading from: %s', self.calendar_file)
        with open(self.calendar_file, 'r') as fp:
            for event in json.load(fp):
                start = datetime.fromisoformat(event['start'])
                end = datetime.fromisoformat(event['end'])
                if not start.tzinfo:
                    start = start.replace(tzinfo=timezone.utc)

                events.append({
                    'start': start,
                    'time': None if start.strftime('%H:%M') == '00:00' else start.strftime('%H:%M'),
                    'days_ahead': (start - utc_time).days + 1,
                    'all_day': start.strftime('%H:%M') == '00:00' and end.strftime('%H:%M') == '00:00',
                    'summary': event['title'],
                })

        events = sorted(
            events,
            key=lambda event: event['start']
        )

        return events
