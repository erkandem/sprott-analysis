import json
from http import HTTPStatus

import pytest

from webapp import ALLOWED_HISTOGRAM_FILES, get_equally_distanced_range_to_zero


@pytest.mark.parametrize(
    "input_data,expected",
    [
        ((-1, 4), (-4, 4)),  # values, which are both below and above zero
        ((-3, -4), (-4, 4)),  # values, which are only negative
        ((1, 4), (-4, 4)),  # values, which are only positive
    ],
)
def test_get_max_max_min_min(input_data, expected):
    result = get_equally_distanced_range_to_zero(input_data)
    assert result == expected


@pytest.mark.parametrize("filename", ALLOWED_HISTOGRAM_FILES)
def test_histogram_route_for_allowed_files(
    client,
    filename,
):
    response = client.get("histogram" + "/" + filename)
    assert response.status_code == HTTPStatus.OK
    assert "Content-Type" in response.headers
    assert response.headers["Content-Type"] == "application/json"


@pytest.mark.parametrize(
    "filename",
    ALLOWED_HISTOGRAM_FILES,
)
def test_histogram_route_schema(client, filename):
    response = client.get("histogram" + "/" + filename)
    assert response.status_code == HTTPStatus.OK
    assert "Content-Type" in response.headers
    assert response.headers["Content-Type"] == "application/json"
    response_data = json.loads(response.data)
    assert isinstance(response_data, dict)
    assert "x" in response_data
    assert isinstance(response_data["x"], list)
    assert isinstance(response_data["x"][0], float)
    assert "y" in response_data
    assert isinstance(response_data["y"], list)
    assert isinstance(response_data["y"][0], int)


def test_histogram_route_for_not_allowed_file(client):
    not_allowed_file = "xyz"
    assert not_allowed_file not in ALLOWED_HISTOGRAM_FILES
    response = client.get("histogram" + "/" + not_allowed_file)
    assert response.status_code == HTTPStatus.NOT_FOUND
