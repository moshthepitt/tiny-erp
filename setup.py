"""
Setup.py for django-tiny-erp
"""
from setuptools import setup, find_packages

SMALL_SMALL_HR_VERSION = __import__('tiny_erp').__small_small_hr_version__

setup(
    name='django-tiny-erp',
    version=__import__('tiny_erp').__version__,
    description='Enterprise Resource Planning (ERP) for tiny companies',
    license='MIT',
    author='Kelvin Jayanoris',
    author_email='kelvin@jayanoris.com',
    url='https://github.com/moshthepitt/tiny-erp',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'Django>=2.0.11',
        f'small_small_hr=={SMALL_SMALL_HR_VERSION}'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)

