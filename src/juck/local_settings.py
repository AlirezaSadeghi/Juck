# -*- coding: utf-8 -*-

DEBUG          = True
TEMPLATE_DEBUG = DEBUG


LOGGING = {
    'loggers': {
        '': {
            'handlers': ['console'], # can be: null, console, mail_admin
            'level': 'WARNING',
            },
        'Juck' : {
            'handlers': ['console'], # can be: null, console, mail_admin
            'level': 'DEBUG',
            },
        'django.request': {
            'handlers': ['console'], # can be: null, console, mail_admin
            #'filters': ['require_debug_false'], # means when debug set to false do logging
            'level': 'WARNING',
            },
        'django.db.backends': { # For performance reasons, SQL logging is only enabled when settings.DEBUG is set to True
			'handlers': ['console'], # can be: null, console, mail_admin
            'level': 'WARNING',
        },
    }
}


BASEPATH      ='/home/alireza/Documents/Juck'
STATIC_ROOT   = BASEPATH + 'static/'
SITE_URL      = 'http://127.0.0.1:8000/'
LOGIN_URL     = '/accounts/login/'

TEMPLATE_DIRS = ( # in here JUST import django admin templates
	'/usr/local/lib/python2.6/dist-packages/Django-1.3.1-py2.6.egg/django/contrib/admin/templates', # for ubuntu 10.04 users with easy_install
	'/usr/local/lib/python2.7/dist-packages/Django-1.3.1-py2.7.egg/django/contrib/admin/templates', # for other ubuntu users with easy_install
	'/usr/local/lib/python2.6/dist-packages/django/contrib/admin/templates', # for ubuntu 10.04 users
	'/usr/local/lib/python2.7/dist-packages/django/contrib/admin/templates', # for other ubuntu users
	'C:/Python27/Lib/site-packages/django/contrib/admin/templates/', # for windows users
)


SERVE_STATIC_FILES = True


SECRET_KEY    = 'alkdj./alekjtl1j35ljad/madgljhad?A?D:GA:DA"GADLg135;kadf'


DATABASES = {
		'default': {
			'ENGINE':   'django.db.backends.sqlite3',
			'NAME':     'reza.sqlite',
			'USER':     'root',
			'PASSWORD': '',
			'HOST':     '',
			'PORT':     '',
			}

}

ADMINS = (
	    ('Alireza Sadeghi', 'sadeghi@arsh.co'),
	)
