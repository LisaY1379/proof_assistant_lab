import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
agent = load('agent', ROOT / 'main/agent_server.py')
batch = load('batch', ROOT / 'workflows/batch_experiments/run_control_vs_rag.py')

class PipelineTests(unittest.TestCase):
    proof = 'Start. Known step. Bridge. New step. Routine x = x. End.'
    graph = {'nodes': [{'id': 'known', 'label': 'Known'}], 'edges': []}
    def responses(self):
        return [
            {'highlights': [
                {'quote': 'Known step.', 'kind': 'library', 'node_id': 'known', 'strategy': 'Known', 'annotation': 'Uses Known.'},
                {'quote': 'New step.', 'kind': 'new', 'node_id': '', 'strategy': 'New', 'annotation': 'Critical construction.'}]},
            {'edits': [
                {'id': 'p1', 'action': 'omit', 'replacement': '', 'reason': 'Routine application.'},
                {'id': 'p2', 'action': 'elaborate', 'replacement': 'New step with the missing justification.', 'reason': 'Crucial detail.'}]},
            {'edits': [{'segment_id': 'u3', 'quote': 'Routine x = x.', 'action': 'omit', 'replacement': '', 'reason': 'Identity calculation.'}]}
        ]
    def run_pipeline(self, responses=None):
        responses = iter(responses or self.responses())
        self.calls = []
        def call(messages):
            self.calls.append(messages)
            return json.dumps(next(responses))
        with patch.object(agent, 'load_graph', return_value=self.graph):
            return agent.run_library_pipeline('Prove it', self.proof, call)
    def test_exact_preservation_and_isolation(self):
        result = self.run_pipeline()
        self.assertEqual(result['answer'], 'Start.  Bridge. New step with the missing justification.  End.')
        self.assertEqual(result['initial_revised'], 'Start.  Bridge. New step with the missing justification. Routine x = x. End.')
        third = json.loads(self.calls[2][1]['content'])
        self.assertEqual(set(third), {'unhighlighted_segments'})
        text = json.dumps(third)
        for forbidden in ['Known step.', 'New step.', 'missing justification', 'Prove it']:
            self.assertNotIn(forbidden, text)
        self.assertEqual(json.loads(self.calls[0][1]['content'])['library'], self.graph)
        self.assertIn('aria-label="Omitted"', result['comparison_html'])
        import re
        ids = set(re.findall(r'id="([^"]+)"', result['comparison_html']))
        for target in re.findall(r'href="#([^"]+)"', result['comparison_html']):
            self.assertIn(target, ids)
    def test_reject_unknown_library(self):
        data = self.responses(); data[0]['highlights'][0]['node_id'] = 'invented'
        with self.assertRaises(ValueError): self.run_pipeline(data)
    def test_reject_changed_source_quote(self):
        data = self.responses(); data[0]['highlights'][0]['quote'] = 'Altered step.'
        with self.assertRaises(ValueError): self.run_pipeline(data)
    def test_reject_node3_targeting_highlight(self):
        data = self.responses(); data[2]['edits'][0]['quote'] = 'Known step.'
        with self.assertRaises(ValueError): self.run_pipeline(data)
    def test_reject_library_elaboration(self):
        data = self.responses(); data[1]['edits'][0].update(action='elaborate', replacement='Longer known step.')
        with self.assertRaises(ValueError): self.run_pipeline(data)
    def test_reject_new_strategy_omission(self):
        data = self.responses(); data[1]['edits'][1].update(action='omit', replacement='')
        with self.assertRaises(ValueError): self.run_pipeline(data)
    def test_reject_duplicate_and_missing_decisions(self):
        for decisions in [[], [self.responses()[1]['edits'][0]] * 2]:
            data = self.responses(); data[1]['edits'] = decisions
            with self.assertRaises(ValueError): self.run_pipeline(data)
    def test_reject_overlapping_annotations(self):
        data = self.responses(); data[0]['highlights'].append(data[0]['highlights'][0])
        with self.assertRaises(ValueError): self.run_pipeline(data)
    def test_no_highlights_is_identity(self):
        result = self.run_pipeline([{'highlights': []}, {'edits': []}, {'edits': []}])
        self.assertEqual(result['answer'], self.proof)
    def test_all_highlighted_node3_has_no_text(self):
        data = self.responses(); data[0]['highlights'] = [dict(data[0]['highlights'][0], quote=self.proof)]
        data[1]['edits'] = [{'id': 'p1', 'action': 'keep', 'replacement': self.proof, 'reason': 'Needed.'}]
        data[2]['edits'] = []
        self.assertEqual(self.run_pipeline(data)['answer'], self.proof)
        self.assertEqual(json.loads(self.calls[2][1]['content']), {'unhighlighted_segments': []})
    def test_model_cannot_override_validated_offsets(self):
        data = self.responses()
        data[1]['edits'][0].update(start=0, end=len(self.proof), quote=self.proof)
        result = self.run_pipeline(data)
        self.assertTrue(result['answer'].startswith('Start.'))
    def test_compression_and_repeated_quote(self):
        self.assertEqual(agent.exact_span('a a a', {'quote':'a', 'occurrence':2}), (4,5))
        data = self.responses()
        data[1]['edits'][0].update(action='compress', replacement='Known.')
        self.assertIn('Known.', self.run_pipeline(data)['answer'])
    def test_overlapping_cleanup_is_rejected(self):
        data = self.responses()
        data[2]['edits'] *= 2
        with self.assertRaises(ValueError): self.run_pipeline(data)
    def test_html_escape(self):
        rendered = agent.render_comparison_html('<script>alert(1)</script>', [], [])
        self.assertNotIn('<script>', rendered)
    def test_batch_reuses_control_and_shared_pipeline(self):
        replies = [json.dumps(r) for r in self.responses()]
        with patch.object(agent, 'load_graph', return_value=self.graph), patch.object(agent, 'call_openai_chat', side_effect=replies) as mock:
            result = batch.call_condition(agent=agent, condition='library_rag', item={'id':'x','statement':'T'}, model='test', reasoning_effort=None, max_completion_tokens=4000, temperature=1, sleep_seconds=0, direct_draft=self.proof)
        self.assertEqual(mock.call_count, 3)
        self.assertEqual(len(result['changes']), 3)
    def test_interactive_shared_pipeline(self):
        replies = [self.proof] + [json.dumps(r) for r in self.responses()]
        with patch.object(agent, 'load_dotenv'), patch.dict(agent.os.environ, {'OPENAI_API_KEY':'test'}), patch.object(agent, 'append_chat_log'), patch.object(agent, 'load_graph', return_value=self.graph), patch.object(agent, 'call_openai_chat', side_effect=replies) as mock:
            result = agent.handle_chat({'mode':'library_rag','message':'Prove it'})
        self.assertEqual(mock.call_count, 4)
        self.assertEqual(len(result['changes']), 3)

if __name__ == '__main__': unittest.main()
