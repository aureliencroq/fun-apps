class ProblemMonitor(object):
    def __init__(self, problem_module, store):
        self.problem_module = problem_module
        self.store = store
        self.ancestors_names = []
        self._get_ancestors_name(problem_module.location)

    def _get_ancestors_name(self, location):
        location = self.store.get_parent_location(location)
        if not location:
            return
        self.ancestors_names.append(self.store.get_item(location).display_name)
        return self._get_ancestors_name(location)

class ProblemFactory
