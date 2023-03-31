from http import HTTPStatus
from pathlib import Path

import numpy as np
import pandas as pd
from flask import Flask, send_from_directory
from flask_cors import CORS


def get_equally_distanced_range_to_zero(data):
    abs_min = abs(min(data))
    abs_max = abs(max(data))
    highest_abs_value = max((abs_min, abs_max))
    return -highest_abs_value, highest_abs_value


ALLOWED_HISTOGRAM_FILES = [
    "esg-gold",
    "gold",
    "gold-and-silver",
    "platinum-and-palladium",
    "silver",
    "uranium",
]
ALLOWED_DOWNLOAD_FILES = [elm + ".json" for elm in ALLOWED_HISTOGRAM_FILES]
HISTOGRAMM_TO_PHYSICAL_FILE_MAPPING = {
    elm: elm + ".json" for elm in ALLOWED_HISTOGRAM_FILES
}

WORKING_DIRECTORY = Path("./").resolve()
DOWNLOAD_DIRECTORY_NAME = "data"
DOWNLOAD_DIRECTORY = WORKING_DIRECTORY / DOWNLOAD_DIRECTORY_NAME


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/premium-discount/<string:filename>")
def resolve_premium_discount_json(filename: str):
    if filename not in ALLOWED_DOWNLOAD_FILES:
        return "", HTTPStatus.NOT_FOUND
    return send_from_directory(DOWNLOAD_DIRECTORY, filename)


@app.route("/histogram/<string:filename>")
def resolve_uranium_histogram(filename):
    if filename not in ALLOWED_HISTOGRAM_FILES:
        return "", HTTPStatus.NOT_FOUND
    file_path = DOWNLOAD_DIRECTORY / HISTOGRAMM_TO_PHYSICAL_FILE_MAPPING[filename]
    df = pd.read_json(file_path)
    return (lambda elm: {"x": elm[1].tolist(), "y": elm[0].tolist()})(
        np.histogram(
            df.premium_pct,
            bins=80,
            range=get_equally_distanced_range_to_zero(df.premium_pct),
        )
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=8080,
    )
