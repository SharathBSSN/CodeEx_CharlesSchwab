import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_valid_dag(client):
    data = {
        "Step1": ["Step2"],
        "Step2": ["Step3"],
        "Step3": []
    }
    response = client.post('/health', json=data)
    assert response.status_code == 200
    assert b'CSV Saved to' in response.data
    assert b'Visualization Path' in response.data

def test_complex_dag(client):
    data = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["E"],
        "D": ["F"],
        "E": ["F"],
        "F": []
    }
    response = client.post('/health', json=data)
    assert response.status_code == 200
    assert b'CSV Saved to' in response.data
    assert b'Visualization Path' in response.data

def test_empty_dag(client):
    data = {}
    response = client.post('/health', json=data)
    assert response.status_code == 200
    assert b'CSV Saved to' in response.data
    assert b'Visualization Path' in response.data

def test_single_node_dag(client):
    data = {"Node1": []}
    response = client.post('/health', json=data)
    assert response.status_code == 200
    assert b'CSV Saved to' in response.data
    assert b'Visualization Path' in response.data

def test_disconnected_dag(client):
    data = {
        "Node1": [],
        "Node2": []
    }
    response = client.post('/health', json=data)
    assert response.status_code == 200
    assert b'CSV Saved to' in response.data
    assert b'Visualization Path' in response.data

def test_invalid_json(client):
    response = client.post('/health', data='invalid json', content_type='application/json')
    assert response.status_code == 400
    assert b'Error' in response.data

def test_large_dag(client):
    large_dag = {f"Node{i}": [f"Node{i+1}"] for i in range(100)}
    large_dag["Node100"] = []
    response = client.post('/health', json=large_dag)
    assert response.status_code == 200
    assert b'CSV Saved to' in response.data
    assert b'Visualization Path' in response.data

# def test_dag_with_self_dependency(client):
#     data = {
#         "A": ["A"]
#     }
#     response = client.post('/health', json=data)
#     assert response.status_code == 200
#     assert b'CSV Saved to' in response.data
#     assert b'Visualization Path' in response.data

def test_dag_with_multiple_root_nodes(client):
    data = {
        "A": ["C"],
        "B": ["D"],
        "C": [],
        "D": []
    }
    response = client.post('/health', json=data)
    assert response.status_code == 200
    assert b'CSV Saved to' in response.data
    assert b'Visualization Path' in response.data

def test_dag_with_cycles_handled(client):
    data = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A"]
    }
    response = client.post('/health', json=data)
    assert response.status_code == 200
    assert b'CSV Saved to' in response.data
    assert b'Visualization Path' in response.data