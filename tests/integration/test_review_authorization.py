def create_author(client, username, email):
    response = client.post(
        "/authors",
        json={
            "lastname": "Petrov",
            "firstname": "Ivan",
            "email": email,
            "username": username,
            "password": "test-password",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def get_access_token(client, username):
    response = client.post(
        "/auth/login",
        data={"username": username, "password": "test-password"},
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


def test_login_and_review_delete_enforce_authenticated_owner(client):
    create_author(client, "bookowner", "owner@example.com")
    review_author = create_author(client, "reviewauthor", "reviewer@example.com")
    owner_headers = {
        "Authorization": f"Bearer {get_access_token(client, 'bookowner')}"
    }
    reviewer_headers = {
        "Authorization": f"Bearer {get_access_token(client, 'reviewauthor')}"
    }

    book_response = client.post(
        "/books",
        json={
            "name": "Shared Book",
            "description": "A book for review",
            "is_shown": True,
        },
        headers=owner_headers,
    )
    assert book_response.status_code == 201, book_response.text
    book_id = book_response.json()["id"]

    unauthenticated_create = client.post(
        f"/books/{book_id}/reviews",
        json={"description": "Good book", "rating": 5},
    )
    assert unauthenticated_create.status_code == 401

    review_response = client.post(
        f"/books/{book_id}/reviews",
        json={"description": "Good book", "rating": 5},
        headers=reviewer_headers,
    )
    assert review_response.status_code == 201, review_response.text
    review_id = review_response.json()["id"]
    assert review_response.json()["author_id"] == review_author["id"]

    forbidden_owner_delete = client.delete(
        f"/books/{book_id}/reviews/{review_id}",
        headers=owner_headers,
    )
    assert forbidden_owner_delete.status_code == 403

    # This path ID differs from the review ID, exposing swapped route arguments.
    forbidden_delete = client.delete(
        f"/books/{book_id}/reviews/{review_author['id']}",
        headers=owner_headers,
    )
    assert forbidden_delete.status_code == 404

    review_still_exists = client.get(
        f"/books/{book_id}/reviews/{review_id}",
        headers=reviewer_headers,
    )
    assert review_still_exists.status_code == 200

    owner_delete = client.delete(
        f"/books/{book_id}/reviews/{review_id}",
        headers=reviewer_headers,
    )
    assert owner_delete.status_code == 204
