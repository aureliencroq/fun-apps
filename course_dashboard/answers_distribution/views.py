from django.http import HttpResponse, Http404
from django.shortcuts import render

import answers_distribution as ad

from opaque_keys.edx.keys import CourseKey
from xmodule.modulestore.django import modulestore

from fun.utils.views import ensure_valid_course_key
from fun.utils.views import staff_required_or_level

@ensure_valid_course_key
@staff_required_or_level('staff')
def index(request, course_id):
    """
    List all course problem modules 
    """
    
    course_key = CourseKey.from_string(course_id)
    store = modulestore()
    
    problem_modules = ad.fetch_modules(course_key, store)
    
    for problem_module in problem_modules:
        ad.add_ancestors_names_to_problem_module(problem_module, store)
        ad.parse_problem_data_from_problem_module(problem_module)

    return render(request, 'course_dashboard/answers_distribution.html', {
        "course_id": course_id,
        "problem_modules" : problem_modules
    })
    
    
@ensure_valid_course_key
@staff_required_or_level('staff')
def get_answers_to_problem_module(request, course_id):
    
    if 'problem_module_id' in request.GET:
        course_key = CourseKey.from_string(course_id)
        store = modulestore()
        qualifiers = {'qualifiers' : {'category' : 'problem',
                                      'name' : request.REQUEST['problem_module_id']}}
        problem_module  = store.get_items(course_key, **qualifiers)
        
        ad.add_answers_distribution_to_problem_module(problem_module[0])

        return render(request, 'course_dashboard/multiplechoice_response.html', {
            "course_id": course_id,
            "problem_module" : problem_module[0]
        })
    else:
        raise Http404
