import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


def pytest_configure(config):
    # Ensure the tests run in consistent locale/encoding context if needed
    pass


@pytest.fixture(scope="function")
def client():
    """TestClient fixture with activities state reset after each test."""
    original_state = copy.deepcopy(activities)
    test_client = TestClient(app)

    try:
        yield test_client
    finally:
        # Reset in-memory activities to original state between tests.
        activities.clear()
        activities.update(copy.deepcopy(original_state))
