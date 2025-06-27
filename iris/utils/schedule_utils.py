from datetime import datetime, timedelta
import calendar

WEEKDAYS = {
    "Mon": 0,
    "Tue": 1,
    "Wed": 2,
    "Thu": 3,
    "Fri": 4,
    "Sat": 5,
    "Sun": 6,
}

def parse_schedule(schedule):
    '''
    Takes a list of strings like ["Mon 09:00", "Wed 11:00"]
    and returns a list of (weekday_number, hour, minute) tuples.
    '''
    parsed = []
    for entry in schedule:
        day_str, time_str = entry.strip().split()
        weekday = WEEKDAYS[day_str]
        hour, minute = map(int, time_str.split(":"))
        parsed.append((weekday, hour, minute))
    return parsed

def generate_class_sessions_from_class(class_, start_date, end_date):

    from website.models import ClassSession  # importing here to avoid circular dependency

    if not class_.schedule:
        raise ValueError("Class.schedule is empty or not set.")

    parsed_schedule = parse_schedule(class_.schedule.split(','))
    current_date = start_date
    sessions = []

    while current_date <= end_date:
        for weekday, hour, minute in parsed_schedule:
            if current_date.weekday() == weekday:
                session_datetime = datetime.combine(current_date, datetime.min.time()).replace(
                    hour=hour, minute=minute)
                sessions.append(ClassSession(class_id=class_.id, date=session_datetime))
        current_date += timedelta(days=1)

    return sessions

''' First implementation of teacher schedule '''
