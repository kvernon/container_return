import http

from configtest import client, app, rentals_repo_mock, rental


def test_get_rentals_by_user_should_be_200(client, app, rentals_repo_mock, rental):
    expected_rentals = [rental]

    rentals_repo_mock.get_rentals_by_user_id.return_value = expected_rentals
    app.container.rental_repository.override(rentals_repo_mock)
    response = client.get(f"/rentals/users/{rental.user_id}")
    assert response.status_code == http.HTTPStatus.OK


def test_get_rentals_by_user_and_nothing(client, app, rentals_repo_mock):
    expected_rentals = []

    rentals_repo_mock.get_rentals_by_user_id.return_value = expected_rentals
    app.container.rental_repository.override(rentals_repo_mock)
    response = client.get(f"/rentals/users/1234--user", content_type='application/json')
    assert response.status_code == http.HTTPStatus.OK


def test_get_rental_by_id_should_return_200(client, app, rentals_repo_mock, rental):
    rentals_repo_mock.get_by_id.return_value = rental

    with app.container.rental_repository.override(rentals_repo_mock):
        response = client.get(f"/rentals/{rental.id}", content_type='application/json')

    assert response.status_code == http.HTTPStatus.OK


def test_get_rental_by_id_should_return_body(client, app, rentals_repo_mock, rental):
    rentals_repo_mock.get_by_id.return_value = rental

    with app.container.rental_repository.override(rentals_repo_mock):
        response = client.get(f"/rentals/{rental.id}", content_type='application/json')

    assert response.data is not None


def test_get_rental_by_id_and_no_rentals_should_be_not_found(client, app, rentals_repo_mock):
    rentals_repo_mock.get_by_id.return_value = None

    with app.container.rental_repository.override(rentals_repo_mock):
        response = client.get(f"/rentals/rental-119", content_type='application/json')

    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_put_rentals_not_found(client, app, rental, rentals_repo_mock):
    rentals_repo_mock.get_by_id.return_value = None
    with app.container.rental_repository.override(rentals_repo_mock):
        response = client.put(f"/rentals/{rental.id}", content_type='application/json')
    assert response.status_code == http.HTTPStatus.NOT_FOUND, response.data


def test_put_rentals_bad_date(client, app, rental, rentals_repo_mock):
    rentals_repo_mock.get_by_id.return_value = rental
    with app.container.rental_repository.override(rentals_repo_mock):
        request_body = dict(return_date="hello")
        response = client.put(f"/rentals/{rental.id}", json=request_body, content_type="application/json")
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_put_rentals_valid_date(client, app, rental, rentals_repo_mock):
    rentals_repo_mock.get_by_id.return_value = rental
    with app.container.rental_repository.override(rentals_repo_mock):
        request_body_valid_date = dict(return_date="2025-03-15T16:30:00Z")
        response = client.put(f"/rentals/{rental.id}", json=request_body_valid_date, content_type="application/json")
    assert response.status_code == http.HTTPStatus.ACCEPTED


def test_put_rentals_found_should_form_event(client, app, rental, rentals_repo_mock):
    rentals_repo_mock.get_by_id.return_value = rental
    with app.container.rental_repository.override(rentals_repo_mock):
        response = client.put(f"/rentals/{rental.id}", content_type='application/json')
    assert response.status_code == http.HTTPStatus.ACCEPTED
