from lxml import etree

from xmodule.modulestore.tests.factories import ItemFactory
from course_dashboard.tests.base import BaseCourseDashboardTestCase
from course_dashboard.answers_distribution_new.problem_monitor import ProblemMonitor
from capa.tests import response_xml_factory as RF

from course_dashboard.answers_distribution_new import question_monitors as QM

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
        
    def _build_problem(self, *args):
        """ Build a problem string.

        Uses *args : A list of string questions generate by ResponseXMLFactory()
        """

        problem = etree.Element("problem")
        for string_question in args:
            xml_question = etree.fromstring(string_question)
            [problem.append(element) for element in xml_question.findall('*')]
        return etree.tostring(problem)

    def test_get_ancestors_names(self):
        pm = ProblemMonitor(self.problem_module, self.store)
        self.assertEqual(pm.ancestors_names, ['vertical', 'sequential',
                                              'chapter', self.course.display_name])


    def test_preprocess_problem(self):
        problem_tree = self._build_problem(RF.MultipleChoiceResponseXMLFactory().build_xml(),
                                           RF.MultipleChoiceResponseXMLFactory().build_xml(),
                                           RF.MultipleChoiceResponseXMLFactory().build_xml())
        self.problem_module.data = problem_tree
        problem_monitor = ProblemMonitor(self.problem_module, self.store)
        for question_monitor in problem_monitor.question_monitors:
            self.assertTrue(isinstance(question_monitor,
                                       QM.MultipleChoiceMonitor))

    def test_preprocess_problem_with_not_handled_question(self):

        problem_tree = self._build_problem(RF.MultipleChoiceResponseXMLFactory().build_xml(),
                                           RF.NumericalResponseXMLFactory().build_xml(),
                                           RF.MultipleChoiceResponseXMLFactory().build_xml())
        self.problem_module.data = problem_tree

        problem_monitor = ProblemMonitor(self.problem_module, self.store)
        question_monitors = problem_monitor.question_monitors

        self.assertEqual(len(question_monitors), 3)
        self.assertTrue(isinstance(question_monitors[0],
                                   QM.MultipleChoiceMonitor))
        self.assertTrue(isinstance(question_monitors[1],
                                   QM.UnhandledQuestionMonitor))
        self.assertTrue(isinstance(question_monitors[2],
                                   QM.MultipleChoiceMonitor))
