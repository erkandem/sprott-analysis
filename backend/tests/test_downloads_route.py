import json
from http import HTTPStatus

import pytest

from webapp import ALLOWED_DOWNLOAD_FILES, DOWNLOAD_DIRECTORY


@pytest.mark.parametrize(
    "filename",
    ALLOWED_DOWNLOAD_FILES,
)
def test_download_available_files(
    client,
    filename,
):
    response = client.get("premium-discount/uranium.json")
    assert response.status_code == HTTPStatus.OK
    assert "Content-Type" in response.headers
    assert response.headers["Content-Type"] == "application/json"


@pytest.mark.parametrize(
    "filename",
    ALLOWED_DOWNLOAD_FILES,
)
def test_schema_of_download_file(
    client,
    filename,
):
    response = client.get("premium-discount" + "/" + filename)
    assert response.status_code == HTTPStatus.OK
    assert "Content-Type" in response.headers
    assert response.headers["Content-Type"] == "application/json"
    response_data = json.loads(response.data)
    assert isinstance(response_data, list)
    assert len(response_data) >= 1
    sample_record = response_data[0]
    assert isinstance(sample_record, dict)
    assert "date" in sample_record
    assert isinstance(sample_record["date"], int)
    assert "premium_pct" in sample_record
    assert isinstance(sample_record["premium_pct"], float)
    assert "price" in sample_record
    assert isinstance(sample_record["price"], float)
    assert "nav" in sample_record
    assert isinstance(sample_record["nav"], float)


def test_download_not_allowed_listed_file(client):
    not_allowed_file = "donotserve"
    not_allowed_file_path = DOWNLOAD_DIRECTORY / not_allowed_file
    with open(not_allowed_file_path, "w") as file:
        file.write('')
    assert not_allowed_file not in ALLOWED_DOWNLOAD_FILES
    assert (DOWNLOAD_DIRECTORY / not_allowed_file).exists()
    response = client.get(f"premium-discount/{not_allowed_file}")
    assert response.status_code == HTTPStatus.NOT_FOUND
