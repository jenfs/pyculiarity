"""
Usage details and source available here: https://github.com/jenfs/pyculiarity.

The original R source and examples are available here: https://github.com/twitter/AnomalyDetection.

Copyright and License

Original Python port Copyright 2015 Nicolas Steven Miller

Original R source Copyright 2015 Twitter, Inc and other contributors

Licensed under the GPLv3
"""

from setuptools import setup, find_packages

setup(
    name='pyculiarity',
    version='0.0.3',
    description='A Python port of Twitter\'s AnomalyDetection R Package.',
    long_description=__doc__,
    url='https://github.com/jenfs/pyculiarity',
    author='Nicolas Steven Miller & Jennifer Flynn',
    author_email='',
    license='GPL',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='data anomaly detection pandas timeseries',
    packages=['pyculiarity'],
    install_requires=['numpy', 'scipy', 'pandas', 'pytz',
                      'statsmodels', 'pyloess'],
    extras_require={
        'test': ['nose', 'mock']
    }
)
