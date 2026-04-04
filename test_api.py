import requests

BASE_URL = "http://hvnhv-35-230-91-10.run.pinggy-free.link"

PREDICT_URL = f"{BASE_URL}/predict"

def print_result(label, response, expect_status=None):
    status = response.status_code
    try:
        body = response.json()
    except Exception:
        body = response.text

    status_ok = (expect_status is None) or (status == expect_status)
    print(f"{body}")
    if not status_ok:
        print(f"Expected status: {expect_status}")
    print()


# NHÓM 1: Endpoint cơ bản
print("=" * 55)
print("Nhóm 1: Endpoint cơ bản")
print("=" * 55)

print_result(
    "GET /",
    requests.get(f"{BASE_URL}/"),
    expect_status=200
)

print_result(
    "GET /health",
    requests.get(f"{BASE_URL}/health"),
    expect_status=200
)

# NHÓM 2: Happy path — câu hỏi có trong data.txt
print("=" * 55)
print("Nhóm 2: Happy path (câu hỏi có trong data.txt)")
print("=" * 55)

print_result(
    "POST /predict",
    requests.post(PREDICT_URL, json={"question": "What is the capital of Vietnam?"}),
    expect_status=200
)

print_result(
    "POST /predict",
    requests.post(PREDICT_URL, json={"question": "What is the largest ocean?"}),
    expect_status=200
)

print_result(
    "POST /predict",
    requests.post(PREDICT_URL, json={"question": "What is the highest mountain in Vietnam?"}),
    expect_status=200
)

# NHÓM 3: Câu hỏi ngoài phạm vi data.txt
print("=" * 55)
print("Nhóm 3: Câu hỏi ngoài phạm vi data.txt")
print("=" * 55)

print_result(
    "POST /predict",
    requests.post(PREDICT_URL, json={"question": "Who is the president of Mars?"}),
    expect_status=200
)

print_result(
    "POST /predict",
    requests.post(PREDICT_URL, json={"question": "What is the population of France?"}),
    expect_status=200
)

# NHÓM 4: Validation lỗi đầu vào 
print("=" * 55)
print("Nhóm 4: Validation lỗi đầu vào")
print("=" * 55)
print_result(
    "POST /predict",
    requests.post(PREDICT_URL, json={"question": ""}),
    expect_status=400
)

print_result(
    "POST /predict",
    requests.post(PREDICT_URL, json={"question": "   "}),
    expect_status=400
)

print_result(
    "POST /predict",
    requests.post(PREDICT_URL, json={}),
    expect_status=422
)

print_result(
    "POST /predict",
    requests.post(PREDICT_URL, data={"question": "What is the capital?"}),
    expect_status=422
)

print_result(
    "POST /predict",
    requests.post(PREDICT_URL, json={"question": 123}),
    expect_status=200
)

# NHÓM 5: Routing sai
print("=" * 55)
print("Nhóm 5: Endpoint không tồn tại")
print("=" * 55)

print_result(
    "GET /unknown",
    requests.get(f"{BASE_URL}/unknown"),
    expect_status=404
)

print_result(
    "GET /predict",
    requests.get(PREDICT_URL),
    expect_status=405
)