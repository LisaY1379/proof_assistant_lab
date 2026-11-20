import hashlib
import os
import unittest
from unittest.mock import patch

from main import bubble_service as service


class BubbleServiceTest(unittest.TestCase):
    def test_only_configured_invite_authorized(self):
        invite = 'unit-test-only'
        with patch.dict(os.environ, BUBBLE_INVITE_HASHES=hashlib.sha256(invite.encode()).hexdigest()):
            self.assertTrue(service.authenticated(invite))
            self.assertFalse(service.authenticated('other'))

    def test_one_inflight_request_per_invite(self):
        with service.allowance('test'):
            with self.assertRaises(OverflowError), service.allowance('test'):
                pass

    def test_service_controls_tools_model_and_storage(self):
        data = dict(input='question',model='other',store=True,tools=[{'type':'other'}],
                    previous_response_id='id',max_output_tokens=10001)
        body = service.build_payload('responses',data)
        self.assertFalse(body['store'])
        self.assertNotIn('previous_response_id',body)
        self.assertEqual(body['tools'],[{'type':'web_search'}])
        self.assertEqual(body['max_output_tokens'],10000)
        self.assertNotEqual(body['model'],'other')

    def test_no_shared_file_or_response_references(self):
        for item in ({'type':'item_reference','id':'example'},
                     {'role':'user','content':[{'type':'input_file','file_id':'example'}]}):
            with self.assertRaises(ValueError):
                service.build_payload('responses',{'input':[item]})
