def create_author(client, username="ivanpetrov", email="ivan@example.com"):
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


def get_access_token(client, username="ivanpetrov"):
    response = client.post(
        "/auth/login",
        data={"username": username, "password": "test-password"},
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


def test_books_list_contains_only_shown_books(client):
    create_author(client)
    headers = {"Authorization": f"Bearer {get_access_token(client)}"}

    hidden_response = client.post(
        "/books",
        json={
            "name": "Hidden Book",
            "description": "Not published",
            "is_shown": False,
        },
        headers=headers,
    )
    shown_response = client.post(
        "/books",
        json={
            "name": "Shown Book",
            "description": "Published",
            "is_shown": True,
        },
        headers=headers,
    )
    assert hidden_response.status_code == 201, hidden_response.text
    assert shown_response.status_code == 201, shown_response.text

    response = client.get("/books")

    assert response.status_code == 200
    assert [book["id"] for book in response.json()] == [shown_response.json()["id"]]
    assert client.get(f"/books/{shown_response.json()['id']}").status_code == 200
    assert client.get(f"/books/{hidden_response.json()['id']}").status_code == 404


def test_reviews_list_and_rating_use_only_shown_reviews(client):
    create_author(client)
    create_author(client, username="reviewer2", email="reviewer2@example.com")
    owner_headers = {"Authorization": f"Bearer {get_access_token(client)}"}
    headers = {"Authorization": f"Bearer {get_access_token(client, 'reviewer2')}"}
    book_response = client.post(
        "/books",
        json={
            "name": "Shown Book",
            "description": "Published",
            "is_shown": True,
        },
        headers=owner_headers,
    )
    assert book_response.status_code == 201, book_response.text
    book_id = book_response.json()["id"]

    shown_response = client.post(
        f"/books/{book_id}/reviews",
        json={
            "description": "Shown review",
            "rating": 2,
            "is_shown": True,
        },
        headers=headers,
    )
    hidden_response = client.post(
        f"/books/{book_id}/reviews",
        json={
            "description": "Hidden review",
            "rating": 5,
            "is_shown": False,
        },
        headers=headers,
    )
    assert shown_response.status_code == 201, shown_response.text
    assert hidden_response.status_code == 201, hidden_response.text
    shown_review_id = shown_response.json()["id"]
    hidden_review_id = hidden_response.json()["id"]

    reviews_response = client.get(f"/books/{book_id}/reviews")
    assert [review["id"] for review in reviews_response.json()] == [shown_review_id]
    assert (
        client.get(f"/books/{book_id}/reviews/{hidden_review_id}").status_code
        == 404
    )
    assert client.get("/books").json()[0]["rating"] == 2.0

    hide_response = client.patch(
        f"/books/{book_id}/reviews/{shown_review_id}",
        json={"is_shown": False},
        headers=headers,
    )

    assert hide_response.status_code == 200, hide_response.text
    assert client.get(f"/books/{book_id}/reviews").json() == []
    assert client.get("/books").json()[0]["rating"] == 0.0
