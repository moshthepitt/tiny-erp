"""
Setup.py for django-tiny-erp
"""
# pylint: disable=bad-continuation
from os import path

from setuptools import find_packages, setup

# read the contents of your README file
with open(
    path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8"
) as f:
    LONG_DESCRIPTION = f.read()

VEGA_ADMIN_VERSION = __import__("tiny_erp").__vega_admin__
SMALL_SMALL_HR_VERSION = __import__("tiny_erp").__small_small_hr_version__

setup(
    name="django-tiny-erp",
    version=__import__("tiny_erp").__version__,
    description="Enterprise Resource Planning (ERP) for tiny companies",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Kelvin Jayanoris",
    author_email="kelvin@jayanoris.com",
    url="https://github.com/moshthepitt/tiny-erp",
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=[
        "Django>=2.1.10",
        f"django-vega-admin=={VEGA_ADMIN_VERSION}",
        f"small_small_hr=={SMALL_SMALL_HR_VERSION}",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Django",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
    ],
)
