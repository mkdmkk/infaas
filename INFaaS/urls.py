from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin

import INFaaS
import contextman
import domainman
import inference
import solutionman
import test
from INFaaS import settings

admin.autodiscover()

urlpatterns = patterns('',
    # INFaaS Console (SaaS)
    url(r'^solution/?$', solutionman.views.render, {"page": "index"}),
    url(r'^solution/(P<page>\w+)$', solutionman.views.render),

    url(r'^domain/?$', domainman.views.render, {"page":"index"}),
    url(r'^domain/(P<page>\w+)$', domainman.views.render),

    url(r'^/?$', INFaaS.views.render, {"page":"index"}),
    url(r'^(?P<page>\w+)$', INFaaS.views.render),

    # Context Visualizer (SaaS)
    # url(r'^app/contextviz/?$', contextviz.views.render, {"page":"index"}),
    # url(r'^app/contextviz/(?P<page>\w+)$', contextviz.views.render),

    # INFaaS APIs (CaaS)
    url(r'^api/contexts$', contextman.views.process), # TODO: Remove!
    url(r'^api/solutions$', solutionman.views.process), # TODO: Get training data
    url(r'^api/domains$', domainman.views.process),
    url(r'^api/users$', domainman.views.process),
    url(r'^api/infer$', inference.views.infer),
    url(r'^api/hello', test.views.hello),

    # Admin Console
    url(r'^admin/', include(admin.site.urls)),

    # Context Acquisition
    # url(r'^cb/acquisition/withings', '......smart_health_toilet.withings.on_authorized'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
