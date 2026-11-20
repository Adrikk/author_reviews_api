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


def get_headers(client, username):
    response = client.post(
        "/auth/login",
        data={"username": username, "password": "test-password"},
    )
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_books_are_public_but_writes_require_owner_authentication(client):
    create_author(client, "bookowner", "owner@example.com")
    create_author(client, "otherauthor", "other@example.com")
    owner_headers = get_headers(client, "bookowner")
    other_headers = get_headers(client, "otherauthor")
    book_data = {
        "name": "Shared Book",
        "description": "A book description",
        "is_shown": True,
    }

    unauthenticated_create = client.post("/books", json=book_data)
    assert unauthenticated_create.status_code == 401

    book_response = client.post("/books", json=book_data, headers=owner_headers)
    assert book_response.status_code == 201, book_response.text
    book_id = book_response.json()["id"]

    assert client.get("/books").status_code == 200
    assert client.get(f"/books/{book_id}").status_code == 200

    forbidden_update = client.patch(
        f"/books/{book_id}",
        json={"name": "Changed name"},
        headers=other_headers,
    )
    forbidden_delete = client.delete(
        f"/books/{book_id}", headers=other_headers
    )
    assert forbidden_update.status_code == 403
    assert forbidden_delete.status_code == 403

    owner_update = client.patch(
        f"/books/{book_id}",
        json={"name": "Updated by owner"},
        headers=owner_headers,
    )
    assert owner_update.status_code == 200, owner_update.text
    assert owner_update.json()["name"] == "Updated by owner"

    owner_delete = client.delete(f"/books/{book_id}", headers=owner_headers)
    assert owner_delete.status_code == 204
