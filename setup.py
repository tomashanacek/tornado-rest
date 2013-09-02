import os
from setuptools import setup
from tornado_rest import __version__

root_dir = os.path.dirname(__file__)

with open(os.path.join(root_dir, "requirements.txt")) as f:
    install_requires = [r.strip() for r in f if "#egg=" not in r]


setup(
    name="tornado-rest",
    version=__version__,
    description=("Tornado REST"),
    author="Tomas Hanacek",
    author_email="tomas.hanacek1@gmail.com",
    packages=["tornado_rest"],
    install_requires=install_requires,
    include_package_data=True,
    test_suite="tornado_rest.tests.all.suite"
)
