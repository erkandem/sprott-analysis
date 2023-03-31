# Back End Application to Scrape and Serve refined Data on Sprotts' Closed End Funds

The application is broken down to two components. 
The first one scrapes data from the Sprott website and stores the valuable information in
a JSON file.

The second component is a Flask webapp which  serves the JSON files created 
using the scraper component and offers additional calculations.

## Scraper 
The logic of the scraper is defined in `scraper.py`.
A selection of closed end funds offered by Sprott are configured in subclasses 
of `SprottWebPageScrapeConfig`.

These subclasses are used to request the HTML files and find the target elements within 
the received HTML files.

Besides a CLI output of some selected metrics the scraper creates JSON files in
the `data` directory. The schema of the JSON file looks like the following example:

```json
[{
    "date":1626739200000,
    "premium_pct":7.19,
    "price":8.98,
    "nav":8.38
}
  //...
]
```

## Web-App

The web-app is a Flask app serving the raw JSON files which the scraper created.
As such, the scraper has to have run at least once.

### Raw JSON files
The raw JSON files are available at the `/premium-discount/<string:filename>'` route.
See the `ALLOWED_DOWNLOAD_FILES` list for available files

### Calculations

For convenience, the web-app provides some derived data based on the data in the scraped 
JSON files.

#### Histogram Route

The histogramm route is available at `/histogram/<string:filename>`
For a given filename it will create a histogram on the premium/discount percentage values.
The bins are currently hardcoded.
The response object looks like the following snipped:
```json
{
  "x": [
    -2,
    -1,
    0,
    1,
    2
  ],
  "y": [
    10,
    14,
    30,
    5
  ]
}
```

`x` refers to the borders of each bin and is adjusted to be of equal in distance from zero.
`y` refers to the amount of observations within the corresponding bin.
Notice, that there is always one more element in the `x` array defining the borders than the `y` array.

We can interpret the sample snipper above as: 
 - 10 observations are between equal or greater than -2 and smaller than -1
 - 14 observations are between equal or greater than -1 and  smaller than 0
 - 30 observations are between equal or greater than 0 and  smaller than 1
 - 5 observations are between equal or greater than 1 and **smaller or equal to** 2

## Setup

Create and activate a Python virtual environment (see python_version)
Install the dependencies for development:

    pip install -r requirements.dev.txt

If it all went well, cd into the location of this README if you are not already there.
In the backend directory, fetch the latest data using:

    python scraper.py

Now, the data directory should be populated with some JSON files.
Start the development server in the activated virtual env with:

    python webapp.py

## Development

Before committing, run mypy

    mypy . 
The Scraper is not covered with type checks yet.

After fixing the mypy errors, run `black` to format the code:

    black .

And finally `isort`:

    isort .

## Tests

To run the tests run:

    pytest

The scraper is not covered with tests yet.

