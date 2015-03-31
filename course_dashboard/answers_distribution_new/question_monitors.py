from capa.registry import TagRegistry
import capa.responsetypes as loncapa_question_types

registry = TagRegistry()

class QuestionMonitor(object):
    def  __init__(self, number, question_tree):
        self.number = number
        self.question_tree = question_tree

@registry.register
class MultipleChoiceMonitor(QuestionMonitor):
    tags = ['multiplechoiceresponse']

@registry.register
class UnhandledQuestionMonitor(QuestionMonitor):
    """Monitor for unhandled questions"""

    loncapa_question_tags = loncapa_question_types.registry.registered_tags()
    monitor_question_tags = registry.registered_tags()
    tags = [tags for tags in loncapa_question_tags if tags not in monitor_question_tags]

