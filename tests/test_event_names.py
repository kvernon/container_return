from src.services.event_names import EventNames


def test_event_names_return_hello():
    assert EventNames.HELLO == "HELLO_EVENT"

def test_event_names_return_rental_return():
    assert EventNames.RENTAL_RETURN == "RENTAL_RETURN_EVENT"

def test_event_names_return_rental_return_complete():
    assert EventNames.RENTAL_RETURN_COMPLETE == "RENTAL_RETURN_COMPLETE_EVENT"