# -*- coding: utf-8 -*-

# Imports #####################################################################

from copy import copy
from mock import patch

from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from contact.views import ContactFormView


# Globals #####################################################################

# Default MITX_FEATURES with contact form feature enabled
MITX_FEATURES_CONTACT_FORM = copy(settings.MITX_FEATURES)
MITX_FEATURES_CONTACT_FORM['ENABLE_CONTACT_FORM'] = True


# Classes #####################################################################

class ContactTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.post_vars = {
                'name': u'John Doe',
                'email': u'john@example.com',
                'phone': u'+33664446505',
                'function': u'Student',
                'inquiry': u'account',
                'body': u'Hello! æêé'
            }

    @override_settings(MITX_FEATURES=MITX_FEATURES_CONTACT_FORM)
    @patch('contact.views.render_to_response')
    def test_contact_form_view_get(self, mock_render_to_response):
        """
        Test contact page display (GET)
        """
        contact_form_view = ContactFormView.as_view()
        request = self.factory.get('/contact/')
        contact_form_view(request)

        self.assertEqual(len(mock_render_to_response.call_args_list), 1)
        mock_call = mock_render_to_response.call_args_list[0][0]
        self.assertEqual(len(mock_call), 2)
        self.assertEqual(mock_call[0], 'contact_form/contact_form.html')
        self.assertEqual(len(mock_call[1]), 2)
        self.assertEqual(mock_call[1]['field_id2name'], {
            'name': 'Name',
            'email': 'Email',
            'body': 'Message',
            'inquiry': 'Inquiry'
        })
        self.assertTrue(mock_call[1]['form'])

        self.assertEqual(len(mail.outbox), 0)

    @override_settings(MITX_FEATURES=MITX_FEATURES_CONTACT_FORM)
    @patch('contact.views.render_to_response')
    def test_contact_form_view_post_missing_fields(self, mock_render_to_response):
        """
        Test contact page display (POST), with missing fields values
        """
        contact_form_view = ContactFormView.as_view()
        request = self.factory.post('/contact/')
        contact_form_view(request)

        self.assertEqual(len(mock_render_to_response.call_args_list), 1)
        mock_call = mock_render_to_response.call_args_list[0][0]
        self.assertEqual(len(mock_call), 2)
        self.assertEqual(mock_call[0], 'contact_form/contact_form.html')
        self.assertEqual(len(mock_call[1]), 2)
        self.assertTrue(mock_call[1]['field_id2name'])
        self.assertTrue(mock_call[1]['form'])

        form = mock_call[1]['form']
        self.assertTrue(form.errors['name'])
        self.assertTrue(form.errors['email'])
        self.assertTrue(form.errors['body'])
        self.assertTrue(form.errors['inquiry'])
        self.assertTrue('function' not in form.errors)
        self.assertTrue('phone' not in form.errors)

        self.assertEqual(len(mail.outbox), 0)

    @override_settings(MITX_FEATURES=MITX_FEATURES_CONTACT_FORM)
    def test_contact_form_view_post_sent(self):
        """
        Test contact page display (POST), all correct & sent
        """
        contact_form_view = ContactFormView.as_view()
        request = self.factory.post('/contact/', self.post_vars)

        self.assertEqual(len(mail.outbox), 0)
        response = contact_form_view(request)
        self.assertEqual(len(mail.outbox), 1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/contact/sent/')
        self.assertEqual(mail.outbox[0].subject, 'Contact request - edX')
        self.assertEqual(mail.outbox[0].body, u'Inquiry: My account\nFrom: John Doe <john@example.com>\nPhone: +33664446505\n\nHello! \xe6\xea\xe9\n')

