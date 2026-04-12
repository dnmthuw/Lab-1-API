import sys
import os
import requests
import pytest
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("URL") or "http://127.0.0.1:8000"

# Cắt dấu gạch chéo cuối nếu có
if BASE_URL and BASE_URL.endswith('/'):
    BASE_URL = BASE_URL[:-1]

# BỘ TEST CASES BẰNG PYTEST
# Cách chạy: pytest tests/test_api.py -v

class TestAPIBasics:
    """NHÓM 1: Endpoint cơ bản & Status máy chủ"""
    
    def test_root_endpoint(self):
        res = requests.get(f"{BASE_URL}/")
        assert res.status_code == 200
        assert "system" in res.json()

    def test_health_check(self):
        res = requests.get(f"{BASE_URL}/health")
        assert res.status_code == 200
        assert res.json().get("status") == "ok"


class TestAPIHappyPath:
    """NHÓM 2: Happy path (Câu hỏi có trong Data)"""
    
    def test_capital_of_vietnam(self):
        res = requests.post(f"{BASE_URL}/predict", json={"question": "What is the capital of Vietnam?"})
        assert res.status_code == 200
        assert "Hanoi" in res.json().get("answer", "")

    def test_largest_ocean(self):
        res = requests.post(f"{BASE_URL}/predict", json={"question": "What is the largest ocean?"})
        assert res.status_code == 200
        assert "Pacific" in res.json().get("answer", "")

    def test_highest_mountain_in_vietnam(self):
        res = requests.post(f"{BASE_URL}/predict", json={"question": "What is the highest mountain in Vietnam?"})
        assert res.status_code == 200
        assert "Fansipan" in res.json().get("answer", "")


class TestAPIOutOfScope:
    """NHÓM 3: Out of scope (Câu hỏi nằm ngoài Data)"""
    
    def test_president_of_mars(self):
        res = requests.post(f"{BASE_URL}/predict", json={"question": "Who is the president of Mars?"})
        assert res.status_code == 200
        assert "i don't know" in res.json().get("answer", "").lower()

    def test_population_of_france(self):
        res = requests.post(f"{BASE_URL}/predict", json={"question": "What is the population of France?"})
        assert res.status_code == 200
        assert "i don't know" in res.json().get("answer", "").lower()


class TestAPIValidation:
    """NHÓM 4: Validation (Bắt lỗi đầu vào sai)"""
    
    def test_empty_question(self):
        res = requests.post(f"{BASE_URL}/predict", json={"question": ""})
        assert res.status_code == 400

    def test_whitespace_question(self):
        res = requests.post(f"{BASE_URL}/predict", json={"question": "   "})
        assert res.status_code == 400

    def test_missing_field(self):
        res = requests.post(f"{BASE_URL}/predict", json={})
        assert res.status_code == 422  # Pydantic validation error

    def test_wrong_format_form_data(self):
        res = requests.post(f"{BASE_URL}/predict", data={"question": "abc"})
        assert res.status_code == 422

    def test_wrong_type_number(self):
        res = requests.post(f"{BASE_URL}/predict", json={"question": 123})
        # Có thể pass qua validation ép kiểu hoặc ném 422
        assert res.status_code in [200, 422]


class TestAPIRouting:
    """NHÓM 5: Routing (Kiểm tra điều hướng đường dẫn API sai)"""
    
    def test_unknown_route(self):
        res = requests.get(f"{BASE_URL}/api/unknown_route_123")
        assert res.status_code == 404

    def test_wrong_method_on_predict(self):
        res = requests.get(f"{BASE_URL}/predict")
        assert res.status_code == 405  # Method Not Allowed