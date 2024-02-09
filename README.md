# PKI Express for Python

Package for using PKI Express on Python

The recommend way to install **PKI Express for Python** is through [PyPi](https://pypi.org/):

    $ pip install pkiexpress

Or informing on your project's `requirements.txt` file:

    pkiexpress==1.10.0

## Documentation

https://docs.lacunasoftware.com/en-us/articles/pki-express/python

## Samples

Please visit the [PKI Express samples repository](https://github.com/LacunaSoftware/PkiExpressSamples/tree/master/Python)
for examples on how to use this library.

## Tests

Tests are included in the ``tests`` folder to provide some understanding about compatibility in later python versions. 
These tests are to be executed alongside a service which signs hashes and nonces with Alan Turing's 
certificate and returns the signature. These tests are not available for any outside tester and are not
to be released alongside the client lib.

To run the tests, use pytest and run the