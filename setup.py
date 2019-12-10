"""Setup.py for django-tiny-erp."""
# pylint: disable=bad-continuation
import os
import sys

from setuptools import find_packages, setup

import tiny_erp

VEGA_ADMIN_VERSION = tiny_erp.__vega_admin_version__
SMALL_SMALL_HR_VERSION = tiny_erp.__small_small_hr_version__

if sys.argv[-1] == "publish":
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/* --skip-existing")
    print("You probably want to also tag the version now:")
    print(f"  git tag -a v{tiny_erp.__version__} -m 'version {tiny_erp.__version__}'")
    print("  git push --tags")
    sys.exit()

# read the contents of your README file
with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"),
    encoding="utf-8",
) as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="django-tiny-erp",
    version=tiny_erp.__version__,
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
        "django-phonenumber-field",
        "phonenumbers",
        "django-prices",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Django",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
    ],
    include_package_data=True,
)
