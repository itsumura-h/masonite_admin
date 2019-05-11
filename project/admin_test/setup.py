from setuptools import setup

setup(
    name="masonite_admin",
    version='0.0.1',
    packages=['admin'],
    install_requires=[
        'masonite',
    ],
    include_package_data=True,
)
