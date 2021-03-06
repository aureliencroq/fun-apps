# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy

from universities.models import University


# themes: Environnement
#         Juridique
#         Management
#         Numérique, technologie
#         Relations internationales
#         Santé Sciences
#         Sciences humaines et sociales


class CourseFilteringForm(forms.Form):
    STATE_CHOICES = (
        ('', pgettext_lazy("Course search form: All states", u"All")),
        ('future', _(u"Incoming")),
        ('current', _(u"Current")),
        ('past', _(u"Past")),
        )

    state = forms.ChoiceField(choices=STATE_CHOICES, required=False, label=_(u"State"))
    #theme = forms.ChoiceField(choices=[], required=False, label=_(u"Theme"))
    university = forms.ChoiceField(choices=[], required=False, label=_(u"University"))

    def __init__(self, *args, **kwargs):
        super(CourseFilteringForm, self).__init__(*args, **kwargs)
        self.fields['university'].choices = [
                ((''), pgettext_lazy("Course search form: All universities", u"All"))
            ] + [(u.code, u.name) for u in University.objects.filter(parent__isnull=True).order_by('name')]
