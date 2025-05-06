import json

from flask import Flask, Response
from python_event_bus import EventBus

from src.api.blueprints import rentals
from src.ioc.injector import Injector
from src.services.event_names import EventNames


def create_app(config_file_path=None, container: Injector = None):
    app = Flask(__name__, instance_relative_config=True)
    app.debug = True

    if container:
        the_container = container
    else:
        the_container = Injector()

    the_container.wire(modules=[rentals])
    app.container = the_container

    if config_file_path:
        app.config.from_file(config_file_path, load=json.load)

    @app.route("/")
    def hello() -> Response:
        return Response("""
            <html>
                <head>
                    <title>Lead Backend Engineer: Coding Challenge</title>
                </head>
                <body>
                    <h1>Lead Backend Engineer: Coding Challenge</h1>
                    <h2>Breakdown</h2>
                    <ul>
                        <li>documentation can be found at: root/docs/README.md</li>
                        <li>there's an api and service</li>
                    </ul>
                </body>
            </html>
        """)

    app.register_blueprint(rentals.bp, url_prefix='/rentals')
    service = the_container.return_service()

    EventBus.subscribe(EventNames.HELLO, hello_event)
    EventBus.subscribe(EventNames.RENTAL_RETURN, service.update_rental)
    EventBus.call(EventNames.HELLO)

    return app

def hello_event():
    print("")
    print("")
    print("===================")
    print("EVENT FIRED Hello World!")
    print("===================")
    print("")
    print("")
