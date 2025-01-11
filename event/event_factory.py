from .event_key import EventKey

def event_factory(event_type, **kwargs):
    event = {EventKey.TYPE: event_type}
    event.update(kwargs)  # Add any additional keyword arguments to the event
    return event
