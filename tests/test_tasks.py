from app.models.task import User

from datetime import datetime, UTC


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "TaskManager API"}
    
def test_create_task(client, db):
    user = User(
        name="Test",
        username="test",
        email="test@test.com",
        password_hash="hash",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    data = {
        "title": "Test task",
        "description": "testing api",
        "status": "pending",
        "user_id": user.id
    }

    response = client.post("/tasks", json=data)

    assert response.status_code == 200

    body = response.json()

    assert body["title"] == "Test task"
    assert body["description"] == "testing api"
    assert body["user_id"] == user.id