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

    (r'^user/new/(?P<tagrfid>[0-9A-Za-z]+)/$','ecoaware.devices.views.newUser'),
    (r'^user/update/$','ecoaware.devices.views.updateUser'),
    (r'^device/new$', 'ecoaware.devices.views.newDevice'),
    (r'^device/list$', 'ecoaware.devices.views.listDevices'),
    url(r'^device/update/(?P<username>[-\w]+)/$', 'ecoaware.devices.views.updateDevice', name='updateDevice'),
    (r'^signin/$','ecoaware.devices.views.sign_in'),
    (r'^privatehome/$','ecoaware.devices.views.privatehome'),
    (r'^graphics/$','ecoaware.devices.views.graphics'),
    (r'^logout/$', 'ecoaware.devices.views.closesession'),
    #(r'^coffeeschart/(?P<ndays>\d+)/$', 'ecoaware.devices.views.coffeeschart' ),
    #(r'^energychart/(?P<ndays>\d+)/$', 'ecoaware.devices.views.energychart' ),
    #(r'^scatterchart/(?P<nhours>\d+)/(?P<ndays>\d+)$', 'ecoaware.devices.views.scatterchart' ),
    (r'^(?P<device>[0-9A-Za-z]+)/coffeeschart/(?P<ndays>\d+)/$', 'ecoaware.devices.views.coffeeschart' ),
    (r'^(?P<device>[0-9A-Za-z]+)/energychart/(?P<ndays>\d+)/$', 'ecoaware.devices.views.energychart' ),
    (r'^(?P<device>[0-9A-Za-z]+)/scatterchart/(?P<nhours>\d+)/(?P<ndays>\d+)$', 'ecoaware.devices.views.scatterchart' ),
    #(r'^reset/$', 'ecoaware.devices.views.resetpassword'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'registration/password_reset_form.html', 'email_template_name':'registration/password_reset_email.html'}),
    url(r'^password_reset_done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'registration/password_reset_confirm.html'}),
    url(r'^password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'registration/password_reset_complete.html'}),
    (r'^(?P<rfid>[0-9A-Z]+)/questionnaire/(?P<module>\d+)/(?P<question>\d+)$', 'ecoaware.devices.views.questionnaire' ),

)

#urlpatterns += patterns('ecoaware.views',
#
#    (r'^hello/$', 'hello'),
#    (r'^time/$', 'current_datetime'),
#    (r'^time/plus/(\d{1,2})/$', 'hours_ahead'),
#)
#
#urlpatterns += patterns('ecoaware.books.views',
#    
#    (r'^search-form/$', 'search_form'),
#    (r'^search/$', 'search'),
#)
#
#urlpatterns += patterns('ecoaware.contact.views',
#   
#    (r'^contact/$', 'contact'),
#)

urlpatterns += patterns('ecoaware.devices.views',
   
    #(r'^device/add/$', 'device_add'),
)


