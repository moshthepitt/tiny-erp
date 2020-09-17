# tiny-erp

[![Build Status](https://api.travis-ci.com/moshthepitt/tiny-erp.svg?branch=master)](https://travis-ci.com/moshthepitt/tiny-erp)

Enterprise Resource Planning (ERP) for tiny companies

## Installation

1. Install the app: `pip install django-tiny-erp`
2. Add the tiny-erp apps to `INSTALLED_APPS`.

   ```py
   INSTALLED_APPS = [
       # the usual django stuff
       "tiny_erp",
       "tiny_erp.apps.locations",
       "tiny_erp.apps.products",
       "tiny_erp.apps.purchases",
       "small_small_hr",
       'model_reviews',
       'django_comments',
   ]
   ```

3. Run `manage.py migrate` so that Django will create the model_review tables.
4. Set up the [django-model-reviews](https://github.com/moshthepitt/django-model-reviews) and [small-small-hr](https://github.com/moshthepitt/small-small-hr) apps.
