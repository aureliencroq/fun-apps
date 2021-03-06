# -*- coding: utf-8 -*-
"""
Common settings for LMS & CMS developpement environments
"""

ENVIRONMENT = 'dev'

CMS_BASE = 'localhost:9001'  # Studio web address
LMS_BASE = 'localhost:9000'  # LMS web address

PREVIEW_LMS_BASE = LMS_BASE

MEDIA_ROOT = "/edx/var/edxapp/uploads"

# do not log to sentry in dev
RAVEN_CONFIG = {
    'dsn': '',
}

DEBUG = True
TEMPLATE_DEBUG = True

# By default don't use a worker, execute tasks as if they were local functions
CELERY_ALWAYS_EAGER = True

################################ LOGGERS ######################################

import logging

# Disable noisy loggers
for pkg_name in ['track.contexts', 'track.middleware', 'dd.dogapi']:
    logging.getLogger(pkg_name).setLevel(logging.CRITICAL)

################################ EMAIL ########################################

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

################################ DEBUG TOOLBAR ################################

DEBUG_TOOLBAR_INSTALLED_APPS = ('debug_toolbar', 'django_extensions',)
DEBUG_TOOLBAR_MIDDLEWARE_CLASSES = (
    'django_comment_client.utils.QueryCountDebugMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
#    'SHOW_TOOLBAR_CALLBACK': lambda _: True,
}

########################### PIPELINE #################################

PIPELINE_SASS_ARGUMENTS = '--debug-info --require {proj_dir}/static/sass/bourbon/lib/bourbon.rb'

########################### DEBUG #################################
TEMPLATE_STRING_IS_INVALID = "__INVALID__"
