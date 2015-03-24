from django.conf.urls import url, patterns, include

urlpatterns = patterns('course_dashboard.answers_distribution.views',
                       url(r'^index/$', 'index', name='index'))


urlpatterns += patterns('course_dashboard.answers_distribution',
                        url(r'^reports_manager/',
                            include('reports_manager.urls',
                                    namespace='reports-manager')))
