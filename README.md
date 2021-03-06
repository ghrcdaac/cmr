# Python CMR Client Library

Python client library that abstracts CMR API calls for search, ingest, update, and deletion of collections and granules.



## Setup

Run:

    $ python setup.py install

Or

    $ pip install -e .

### Usage

Populate your CMR credentials into a `cmr.cfg` file, using `cmr.cfg.example` as a template. Alternatively, on instantiation, if no CFG file is provided then the CMR object will load credentials from these environment variables: `CMR_PROVIDER`, `CMR_USERNAME`, `CMR_PASSWORD`, and `CMR_CLIENT_ID`.

Then, run:

```python
$ python
>>> from pyCMR.pyCMR import CMR
>>> cmr = CMR('/path/to/my/cmr.cfg')  # or `cmr = CMR()` to load from env vars
```

## Test

```bash
python setup.py test
```
