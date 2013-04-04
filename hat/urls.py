from django.conf.urls import patterns, include, url

from users import register, login, logout, profile
import json

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from views import main, words, delete_word, save_words, request_words, create_game, new_result_game, send_result_game
import settings

urlpatterns = patterns('',
	url(r'^$', main),
	url(r'^register/$', register),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^profile/$', profile),
    url(r'^words/', words),
    url(r'^delete_word/', delete_word),
    url(r'^save_words/', save_words),
    url(r'^request_words/', request_words),
    url(r'^create_game/', create_game),
    url(r'^new_result_game/', new_result_game),
    url(r'^send_result_game/', send_result_game),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
    # Examples:
    # url(r'^$', 'hat.views.home', name='home'),
    # url(r'^hat/', include('hat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
