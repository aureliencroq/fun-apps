from xmodule.modulestore.tests.factories import ItemFactory
from course_dashboard.tests.base import BaseCourseDashboardTestCase
from course_dashboard.answers_distribution.problem_monitor import ProblemMonitor

class ProblemMonitorTestCase(BaseCourseDashboardTestCase):


    def setUp(self):
        super(ProblemMonitorTestCase, self).setUp()
        self.problem_module = None
        self._generate_modules_tree(self.course,
                                    'chapter', 'sequential',
                                    'vertical', 'problem')

    def _generate_modules_tree(self, module, *args):
        if not args:
            self.problem_module = module
            return
        category = args[0]
        self._generate_modules_tree(ItemFactory(parent=module,
                                                category=category,
                                                display_name=category),
                                    *args[1:])

    def test_get_ancestors_names(self):
        pm = ProblemMonitor(self.problem_module, self.store)
        self.assertEqual(pm.ancestors_names, ['vertical', 'sequential',
                                              'chapter', self.course.display_name])
