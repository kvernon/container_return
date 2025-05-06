import json
from datetime import datetime
from http import HTTPStatus

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, request, Response
from python_event_bus import EventBus

from repositories.rentals_repository import RentalsRepository
from src.encoders.map_to_event import map_to_event
from src.ioc.injector import Injector
from src.services.event_names import EventNames

bp = Blueprint("rentals", __name__)

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "return_date": {
            "type": "string",
            "format": "date-time",
        }
    },
    "required": ["return_date"],
}


@bp.route("/users/<user_id>", methods=['GET'])
@inject
def index(user_id: str, rental_repository: RentalsRepository = Provide[Injector.rental_repository]) -> Response:
    found_items = rental_repository.get_rentals_by_user_id(user_id)
    dicts = [the_rental.to_dict() for the_rental in found_items]
    return Response(json.dumps(dicts), HTTPStatus.OK)


@bp.route('/<rental_id>', methods=['GET'])
@inject
def get_by_id(rental_id: str, rental_repository: RentalsRepository = Provide[Injector.rental_repository]):
    found = rental_repository.get_by_id(rental_id)

    if found is None:
        return Response(status=HTTPStatus.NOT_FOUND)

    return Response(json.dumps(found.to_dict()), HTTPStatus.OK)


@bp.route("/<rental_id>", methods=['PUT'])
@inject
def update(rental_id: str, rental_repository: RentalsRepository = Provide[Injector.rental_repository]) -> Response:
    body = None

    if request.is_json:
        # GET BODY
        body = request.get_json(silent=True)

        if body and 'return_date' in body:
            try:
                return_date_value = body['return_date']
                print(f"body.return_date {return_date_value}")
                body['return_date'] = datetime.fromisoformat(return_date_value.replace("Z", ""))
                print(f"return_date updated: {body['return_date']}")
            except ValueError:
                return Response(status=HTTPStatus.BAD_REQUEST)

    try:

        rental = rental_repository.get_by_id(rental_id)

        if rental is None:
            raise ValueError("Rental Not Found")

        event = map_to_event(
            rental.user_id,
            rental.asset_id,
            rental.created_at_location_id
        ) if body is None else map_to_event(
            rental.user_id,
            rental.asset_id,
            rental.created_at_location_id,
            body['return_date'].isoformat())

        EventBus.call(EventNames.RENTAL_RETURN, event)
        return Response(None, status=HTTPStatus.ACCEPTED)
    except ValueError:
        return Response(status=HTTPStatus.NOT_FOUND)
