from setuptools import setup

setup(
    name="indicators",
    version="0.2",
    packages=['indicators'],
    install_requires=[
        "ta==0.11.0","yfinance==0.2.57","urllib3==1.26.6"
    ],
)
