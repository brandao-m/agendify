from datetime import datetime, timedelta

def generate_slots(start_time, end_time, duration_minutes):

    slots = []

    current = datetime.combine(datetime.today(), start_time)
    end = datetime.combine(datetime.today(), end_time)

    while current + timedelta(minutes=duration_minutes) <= end:

        slots.append(current.time())

        current += timedelta(minutes=duration_minutes)

        return slots