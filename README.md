# Python OTel Sample App

This is an extremely simple Python app that makes an instrumented call to the S3 `ListBuckets` API. It exports the resulting span using
the default OTLP exporter and prints it to the console for debugging.

## Prerequisites

Python 3 and pip installed.

## Usage

1. Clone this repo and navigate into it
2. `pip install requirements.txt`
3. `python sample.py`
