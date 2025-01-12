def event_factory(event_type, **kwargs):
    event = {"type": event_type}
    event.update(kwargs)  # Add any additional keyword arguments to the event
    return event
