from lxml import etree

import capa.responsetypes as loncapa_question_types

import question_monitors 

class ProblemMonitor(object):
    def __init__(self, problem_module, store):
        self.problem_module = problem_module
        self.problem_tree = etree.XML(problem_module.data)
        self.store = store

        self.ancestors_names = []
        self.question_monitors = []

        self._get_ancestors_name(problem_module.location)
        self._preprocess_problem()

    def _get_ancestors_name(self, location):
        location = self.store.get_parent_location(location)
        if not location:
            return
        self.ancestors_names.append(self.store.get_item(location).display_name)
        return self._get_ancestors_name(location)

    def _preprocess_problem(self):
        """
        Parse xml problem tree and instanciate a QuestionMonitor object for each question in the problem
        and store it in self.question_monitors.
        """
        for count, question in enumerate(self.problem_tree.xpath('//' + "|//".join(loncapa_question_types.registry.registered_tags()))):
            question_monitor_cls = question_monitors.registry.get_class_for_tag(question.tag)
            self.question_monitors.append(question_monitor_cls(count, question))
