from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from INFaaS import settings

admin.autodiscover()

urlpatterns = patterns('',
    # INFaaS Console
    url(r'^solution/?$', 'solutionman.views.render', {"page":"index"}),
    url(r'^solution/(P<page>\w+)$', 'solutionman.views.render'),

    url(r'^domain/?$', 'domainman.views.render', {"page":"index"}),
    url(r'^domain/(P<page>\w+)$', 'domainman.views.render'),

    url(r'^/?$', 'INFaaS.views.render', {"page":"index"}),
    url(r'^(?P<page>\w+)$', 'INFaaS.views.render'),

    # Context Visualizer
    url(r'^app/contextviz/?$', 'contextviz.views.render', {"page":"index"}),
    url(r'^app/contextviz/(?P<page>\w+)$', 'contextviz.views.render'),

    # Unit Services; Context Mgt., Solution Mgt., Domain Mgt., User Mgt., and Inference Engine
    url(r'^api/context$', 'contextman.views.process'),
    url(r'^api/solution$', 'solutionman.views.process'),
    url(r'^api/domain$', 'domainman.views.process'),
    url(r'^api/user$', 'domainman.views.process'),
    url(r'^api/infer$', 'inference.views.infer'),

    # Admin Console
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
