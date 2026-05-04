import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app import models

# Тестовая БД
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }

def test_register(client, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]

def test_login(client, test_user):
    # Регистрируем
    client.post("/auth/register", json=test_user)
    
    # Логинимся
    response = client.post("/auth/login", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]

def test_protected_endpoint_requires_auth(client):
    # Доступ без токена
    response = client.get("/plates/")
    assert response.status_code == 401

def test_create_plate(client, test_user):
    # Получаем токен
    client.post("/auth/register", json=test_user)
    login_response = client.post("/auth/login", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    
    # Создаем категорию
    db = TestingSessionLocal()
    category = models.PlateCategory(
        name="Токарные",
        description="Для токарной обработки",
        hardness_range="HRC 40-55"
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    category_id = category.id
    db.close()
    
    # Создаем пластину
    plate_data = {
        "name": "CNMG120408",
        "material": "Карбид",
        "coating": "TiAlN",
        "price": 1250.0,
        "stock_quantity": 100,
        "material_group": "P",
        "max_depth_mm": 6.0,
        "recommended_speed_m_min": 250,
        "category_id": category_id
    }
    
    response = client.post(
        "/plates/",
        json=plate_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == plate_data["name"]
    assert data["category_id"] == category_id

def test_select_plate_algorithm(client, test_user):
    # Получаем токен
    client.post("/auth/register", json=test_user)
    login_response = client.post("/auth/login", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    
    # Создаем категорию
    db = TestingSessionLocal()
    category = models.PlateCategory(
        name="Токарные",
        description="Тест",
        hardness_range="HRC 40"
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    category_id = category.id
    
    # Добавляем тестовые пластины
    plates_data = [
        models.CuttingPlate(
            name="CNMG120408-R",
            material="Карбид",
            coating="TiAlN",
            price=1250,
            stock_quantity=50,
            material_group="P",
            max_depth_mm=6.0,
            recommended_speed_m_min=250,
            category_id=category_id
        ),
        models.CuttingPlate(
            name="WNMG080408-F",
            material="Керамика",
            coating=None,
            price=2100,
            stock_quantity=30,
            material_group="M",
            max_depth_mm=4.0,
            recommended_speed_m_min=350,
            category_id=category_id
        )
    ]
    
    for plate in plates_data:
        db.add(plate)
    db.commit()
    db.close()
    
    # Тестируем алгоритм подбора
    selection_request = {
        "material_group": "P",
        "cutting_depth_mm": 3.5,
        "operation_type": "черновая",
        "max_price": 1500
    }
    
    response = client.post(
        "/select/plate",
        json=selection_request,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert data["total_found"] > 0
    assert data["algorithm_version"] == "v1.0"