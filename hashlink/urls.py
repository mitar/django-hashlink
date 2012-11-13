from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url('^$', 'hashlink.views.hashlink_view', name='hashlink'),
)
