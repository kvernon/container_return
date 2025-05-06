## Notes

### Architecture

In the examples here, there are 2 core ideas

* an event service bus
* lambda who subscribe to the bus.

### Running

run the api

```bash
flask --app src/api/main.py run --port=3211
```

## The purpose of this is to show

1. eventing
2. updating records
3. getting record information back

## Structure of the project

The breakdown around this is again, to show eventing, however, it's also to illustrate microservices. Microservices come
in many forms:

* api
* clustered
* domain oriented

In here, these microservices will be represented as clustered and domain oriented. They could be bundled in a docker
container and thrown in an ECS / EKS AWS type environment. In my career, I've done these both ways, lambda + api gateway
and docker containers. There are trade-offs with both between uptime and cost.

This set up is around grouped domain microservices. In this scenario, it would be put in a container, and run via ECS or EKS. 

If given a larger opportunity this could be structured as lambda + api-gateway focused releases

+ shared libraries over core items Rental, User, Assets
+ extract methods to isolated files (versus the flask + blueprint setup)
+ setup api-gateway to account for execution associations + endpoints between it and the lambda (and of course staging custom-domains)
+ setup cloudwatch to associate for strong tracking of behavior occurring in these 

## Calling

The API is currently written out to look at [rentals](../src/api/blueprints/rentals.py)

Currently, there are 3 endpoints:

1. GET /rentals/:rental_id -- retrieve a rental
2. PUT /rentals/:rental_id -- update a rental by throwing it on the event bus
3. GET /rentals/users/:user_id -- get a user's rentals

## EventBus

In this example I use `python_event_bus`. It gets started in the app, and it gets used in the [`ReturnService`](../src/services/return_service.py)

1. there are basic checks for the put request
2. there are more check within the event object and the service itself.
3. Once things complete it will send a "RENTAL_RETURN_COMPLETE_EVENT" event.
   + Event names can be found at [`EventNames`](../src/services/event_names.py)
   + this can be used to inform other listeners that the service completed successfully
   + others could tie off of things for additional tracking metrics or notifications

## Architecture

I wound up going with flask (it was the one I know of more, I'd probably explore FastAPI in the future). I also tried to break this down in manageable sections and include inversion of control.

To help make some of this work, I had to create wrapper db classes where I could inject the [jojanga_queries](../jojanga_queries). From there I could create the needing bindings.

### Tests

Tests are set up using pytest. I also wound up using [PyCrunch](https://github.com/gleb-sevruk/pycrunch-engine) to run the concurrently

```bash
python -m pytest tests
```

```bash
..............................................                                                                                                                                                                                                                                                               [100%]
46 passed in 0.42s

```