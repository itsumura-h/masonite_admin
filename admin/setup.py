from setuptools import setup

setup(
    name="masonite-admin",
    version='0.0.1',
    packages=['admin'],
    install_requires=[
        'masonite',
        'masonite-api'
    ],
    include_package_data=True,
)
