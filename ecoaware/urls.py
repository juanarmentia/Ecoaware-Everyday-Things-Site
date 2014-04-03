from django.conf.urls import *
from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import os 
site_media = os.path.join( 
    os.path.dirname(__file__),  'site_media' 
)

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('django.contrib.auth.urls')),

    url(r'^user/new/(?P<tagrfid>[0-9A-Za-z]+)$','ecoaware.devices.views.newUser', name='newUser'),
    url(r'^user/update$','ecoaware.devices.views.updateUser', name='updateUser'),
    url(r'^device/new$', 'ecoaware.devices.views.newDevice', name='newDevice'),
    url(r'^device/list$', 'ecoaware.devices.views.listDevices', name='listDevices'),
    url(r'^device/update/(?P<username>[-\w]+)$', 'ecoaware.devices.views.updateDevice', name='updateDevice'),
    url(r'^$','ecoaware.devices.views.sign_in', name='sign_in'),
    url(r'^privatehome$','ecoaware.devices.views.privatehome', name='privatehome'),
    url(r'^graphics$','ecoaware.devices.views.graphics', name='graphics'),
    url(r'^conditions$','ecoaware.devices.views.conditions', name='conditions'),
    url(r'^logout$', 'ecoaware.devices.views.closesession', name='closesession'),
    url(r'^(?P<device>[0-9A-Za-z]+)/coffeeschart/(?P<ndays>\d+)$', 'ecoaware.devices.views.coffeeschart', name='coffeeschart'),
    url(r'^(?P<device>[0-9A-Za-z]+)/energychart/(?P<ndays>\d+)$', 'ecoaware.devices.views.energychart', name='energychart'),
    url(r'^(?P<device>[0-9A-Za-z]+)/scatterchart/(?P<nhours>\d+)/(?P<ndays>\d+)$', 'ecoaware.devices.views.scatterchart', name='scatterchart'),
    url(r'^password_reset$', 'django.contrib.auth.views.password_reset', {'template_name': 'registration/password_reset_form.html', 'email_template_name':'registration/password_reset_email.html'}, name='password_reset'),
    url(r'^password_reset_done$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'registration/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^password_reset_complete$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'registration/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^(?P<rfid>[0-9A-Z]+)/questionnaire/(?P<module>\d+)/(?P<question>\d+)$', 'ecoaware.devices.views.questionnaire', name='questionnaire'),

)

urlpatterns += patterns('ecoaware.devices.views',
   
    #(r'^device/add/$', 'device_add'),
)


