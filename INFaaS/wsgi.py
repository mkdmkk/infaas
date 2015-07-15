"""
WSGI config for SituationInferenceService project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "INFaaS.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from acquisition.withings import WithingsAcquisition

# Acquisition Setting
w = WithingsAcquisition(
    consumer_key="f853b4e9edc1fc75e367fbb60c1b5ff2833b16e2d34d3d5f99055bb560d",
    consumer_secret="7688c3b463e55680b7f069743f364011d3dd66011ce7cb1603cf2787d")
w.connect()