import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from main import app, get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_task(client: TestClient):
    response = client.post("/tasks", json={"title": "Comprar pão"})
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Comprar leite"
    assert data["done"] is False
    assert data["id"] is not None


def test_list_tasks(client: TestClient):
    client.post("/tasks", json={"title": "Tarefa 1"})
    client.post("/tasks", json={"title": "Tarefa 2"})

    response = client.get("/tasks")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2


def test_delete_task(client: TestClient):
    create_response = client.post("/tasks", json={"title": "Apagar"})
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200

    list_response = client.get("/tasks")
    assert len(list_response.json()) == 0


def test_delete_nonexistent_task(client: TestClient):
    response = client.delete("/tasks/999")
    assert response.status_code == 404