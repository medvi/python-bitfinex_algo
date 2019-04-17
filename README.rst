========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-bitfinex_algo/badge/?style=flat
    :target: https://readthedocs.org/projects/python-bitfinex_algo
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/medvi/python-bitfinex_algo.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/medvi/python-bitfinex_algo

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/medvi/python-bitfinex_algo?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/medvi/python-bitfinex_algo

.. |requires| image:: https://requires.io/github/medvi/python-bitfinex_algo/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/medvi/python-bitfinex_algo/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/medvi/python-bitfinex_algo/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/medvi/python-bitfinex_algo

.. |version| image:: https://img.shields.io/pypi/v/bitfinex-algo.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/bitfinex-algo

.. |commits-since| image:: https://img.shields.io/github/commits-since/medvi/python-bitfinex_algo/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/medvi/python-bitfinex_algo/compare/v0.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/bitfinex-algo.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/bitfinex-algo

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/bitfinex-algo.svg
    :alt: Supported versions
    :target: https://pypi.org/project/bitfinex-algo

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/bitfinex-algo.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/bitfinex-algo


.. end-badges

Trading robot

* Free software: BSD 2-Clause License

Installation
============

::

    pip install bitfinex-algo

Documentation
=============


https://python-bitfinex_algo.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
