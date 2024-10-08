from setuptools import setup

setup(
    name='analyzer',
    version='0.1',
    description='a package for time series analysis',
    author='Alina Maksimova',
    author_email='alinamax910@gmail.com',
    packages=['functions_for_analysis'],
    install_requires=[
        'numpy',
        'pandas',
        'meteostat',
        'statsmodels',
        'openpyxl',
    ],
)