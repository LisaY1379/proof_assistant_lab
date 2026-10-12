import copy
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from main import explorer_pipeline as p
from main.explorer_service import ExplorerService

ROOT = Path(__file__).resolve().parents[1]
PROOF = 'Let a=2m and b=2n. Then a+b=2(m+n), so the sum is even.'


def fixture():
    raw = {'title':'Sum of even integers','statement':'The sum of two even integers is even.',
            'nodes':[{'id':'f1','kind':'fact','text':'a and b are even integers'},
                     {'id':'g1','kind':'goal','text':'a+b is even'},
                     {'id':'f2','kind':'fact','text':'a=2m and b=2n for integers m,n'},
                     {'id':'f3','kind':'fact','text':'a+b=2(m+n), m+n is an integer'},
                     {'id':'o1','kind':'observation','text':'The goal asks for a factor of 2'}],
            'initial_facts':['f1'],'initial_goals':['g1'],
            'steps':[{'id':'a1','title':'Unpack evenness','quote':'Let a=2m and b=2n.',
                      'uses':['f1'],'adds':['f2'],'opens':[],'closes':[],'observations':[],
                      'justification':'Definition of even','observation':'Evenness is divisibility by two.',
                      'explanation':'Choose integer witnesses m and n.','difficulty':'Definition use.',
                      'short_version':'Write a=2m and b=2n for integers m,n.'},
                     {'id':'a2','title':'Factor out two','quote':'Then a+b=2(m+n), so the sum is even.',
                      'uses':['f2'],'adds':['f3'],'opens':[],'closes':['g1'],'observations':['o1'],
                      'justification':'Integer closure and definition of evenness.',
                      'observation':'A common factor of two matches the goal.',
                      'explanation':'a+b=2m+2n=2(m+n). Since m+n is an integer, the sum is even.',
                      'difficulty':'Recognize the factor requested by the goal.',
                      'short_version':'a+b=2(m+n) is even.'}]}


    raw['protocol'] = {'version':'0.1', 'context':{
        'domains':'a,b,m,n are integers; a and b are even.',
        'definitions':'An integer is even iff it equals twice an integer.',
        'basic_rules':'B-D definitions, B-C substitution/expansion, B-L logical matching.',
        'toolkit':[{'id':'t1','name':'Integer addition closure',
                    'statement':'m+n is an integer for integers m,n.', 'hypotheses':'m,n are integers.'}]}}
    def action(key, kind, move, verifies=None):
        return {'id':key, 'kind':kind, 'role':'representation' if kind=='strategic' else 'execution',
                'move':move, 'provenance':'Definition or target-directed common-factor observation.',
                'rule':'B-D evenness' if kind=='B-D' else 'Choose representation' if kind=='strategic' else 'B-C expansion and B-L witness introduction',
                'inputs':'a=2m, b=2n and integers m,n' if key!='u1' or kind=='strategic' else 'a,b even',
                'toolkit_uses':[], 'verification':move, 'verifies':verifies or []}
    for i, step in enumerate(raw['steps']):
        step['protocol'] = {
            'direction':'forward' if i==0 else 'meeting',
            'context':'a,b are even integers.' if i==0 else 'a=2m, b=2n with integer witnesses m,n.',
            'target':'a+b is twice an integer.',
            'basic_progress':'Unpack evenness; substitute a=2m and b=2n.',
            'remaining_gap':'None for definition unpacking.' if i==0 else 'Choose an integer witness for the sum.',
            'observation':{'target_feature':'Twice an integer', 'available_feature':'Both summands have factor two',
                           'connection':'The common factor suggests the witness m+n.'},
            'actions':[action('u1','B-D','Name integer witnesses m,n from evenness.')] if i==0 else [
                action('u1','strategic','Choose k=m+n and representation 2(m+n).'),
                action('u2','B-C','Expand 2(m+n)=2m+2n=a+b.', ['u1']),
                action('u3','B-L','Integer closure gives m+n an integer; introduce the evenness witness.', ['u1'])],
            'relation':{'kind':'deduction' if i==0 else 'meeting',
                        'justification':step['justification'], 'side_conditions':'m,n are integers; existential witnesses remain local to the proof.'},
            'remaining_obligations':'Show a+b is even.' if i==0 else 'None.'}
    raw['steps'][1]['protocol']['actions'][2]['toolkit_uses']=[{'id':'t1','hypotheses_check':'m,n are integer witnesses from the definition.'}]
    return raw


def study(origin='model_proposed',sources=None):
    return {'restriction':'No explicit factorization into two times an integer anywhere.',
            'alternatives':[{'title':'Parity classes','origin':origin,'source_ids':sources or [],
                             'adaptation':'Use addition in Z/2Z.',
                             'route':[{'title':'Take residue classes','have':'[a]=[b]=0, so [a+b]=0.','want':''}],
                             'argument':'The quotient map to Z/2Z is additive, so the sum is in its kernel 2Z.',
                             'outcome':'closed','rejoin_state':None,
                             'assessment':'All target obligations are discharged using the quotient-group theorem.',
                             'cost':'A stronger algebraic toolkit; search difficulty unmeasured.'}]}


class ExplorerTests(unittest.TestCase):
    def setUp(self):
        self.doc=p.derive_document(fixture(),PROOF)
        self.research={'status':'disabled','sources':[],'calls':[],'summary':'No search.'}

    def test_graphs_and_closure_share_transitions(self):
        self.assertEqual(self.doc['states'][-1]['want'],[])
        self.assertTrue(self.doc['closure'])
        self.assertEqual(self.doc['states'][1]['action'],'a1')
        self.assertTrue(any(e['kind']=='meeting' and e['to']=='g1' for e in self.doc['proof_edges']))
        self.assertEqual(self.doc['original_proof'],PROOF)

    def test_protocol_is_required_for_new_generation_but_legacy_imports_work(self):
        legacy=fixture();legacy.pop('protocol')
        for step in legacy['steps']:step.pop('protocol')
        with self.assertRaisesRegex(ValueError,'protocol'):
            p.derive_document(legacy,PROOF,require_protocol=True)
        saved=p.derive_document(legacy,PROOF)
        self.assertNotIn('protocol',p.validate_import(saved))

    def test_protocol_rejects_missing_choice_verification_and_hypotheses(self):
        mutations=[
            lambda d:d['steps'][1]['protocol'].pop('remaining_gap'),
            lambda d:d['steps'][1]['protocol']['observation'].pop('connection'),
            lambda d:d['steps'][1]['protocol'].update(actions=d['steps'][1]['protocol']['actions'][:1]),
            lambda d:d['steps'][1]['protocol']['actions'][1].update(verifies=['u3']),
            lambda d:d['steps'][1]['protocol']['actions'][2]['toolkit_uses'][0].update(id='unknown'),
            lambda d:d['steps'][1]['protocol']['actions'][2]['toolkit_uses'][0].pop('hypotheses_check'),
            lambda d:d['steps'][1]['protocol']['relation'].update(kind='sufficient'),
            lambda d:d['steps'][1]['protocol']['actions'][0].update(kind='unresolved')]
        for mutate in mutations:
            raw=fixture();mutate(raw)
            with self.subTest(raw=raw),self.assertRaises(ValueError):
                p.derive_document(raw,PROOF,require_protocol=True)

    def test_actual_protocol_reaches_model_and_is_saved_with_export(self):
        replies=iter([fixture(),study(),study(),{'steps':['a2'],'rationale':'Factor.'}]);calls=[]
        def ask(instruction,data):calls.append(instruction);return next(replies)
        result=p.run_pipeline(PROOF,4,ask,lambda *_:self.research,lambda *_:None,lambda:False)
        reference=p.load_protocol()
        self.assertIn(reference['text'],calls[0])
        self.assertIn('Basic first. Observe when blocked.',calls[0])
        self.assertIn('B-D · Direct definition interpretation',calls[0])
        self.assertEqual(result['protocol']['reference']['sha256'],reference['sha256'])
        imported=p.validate_import(result)
        self.assertEqual(imported['steps'][1]['protocol'],result['steps'][1]['protocol'])
        self.assertEqual(imported['protocol']['reference'],reference)

    def test_missing_protocol_triggers_bounded_correction(self):
        bad=fixture();bad.pop('protocol')
        replies=iter([bad,fixture(),study(),study(),{'steps':['a2'],'rationale':'Factor.'}]);calls=[]
        def ask(instruction,data):calls.append(data);return next(replies)
        result=p.run_pipeline(PROOF,4,ask,lambda *_:self.research,lambda *_:None,lambda:False)
        self.assertIn('protocol',calls[1]['validation_error'])
        self.assertIn('protocol',result)

    def test_preserves_unquoted_material_and_unicode(self):
        doc=p.derive_document(fixture(),'ℕ 😀\n'+PROOF+'\nQED')
        self.assertEqual(doc['steps'][0]['start'],4)
        for s in doc['steps']:
            self.assertEqual(doc['original_proof'][s['start']:s['end']],s['quote'])

    def test_rejects_future_facts_unknown_ids_and_overlapping_quotes(self):
        for mutate in [lambda d:d['steps'][0].update(uses=['f3']),
                       lambda d:d['steps'][0].update(adds=['unknown']),
                       lambda d:d['steps'][1].update(quote='Let a=2m and b=2n.'),
                       lambda d:d['nodes'][1].update(id='f1')]:
            raw=fixture();mutate(raw)
            with self.assertRaises(ValueError):p.derive_document(raw,PROOF)

    def test_incomplete_proof_does_not_claim_closure(self):
        raw=fixture();raw['steps'][1]['closes']=[]
        raw['steps'][1]['protocol']['direction']='forward'
        raw['steps'][1]['protocol']['relation']['kind']='deduction'
        self.assertFalse(p.derive_document(raw,PROOF)['closure'])

    def test_search_provenance_comes_from_tool_metadata(self):
        response={'id':'r1','output':[
            {'type':'web_search_call','id':'search','status':'completed','action':{'type':'search','sources':[{'url':'https://example.org/paper','title':'Paper'}]}},
            {'type':'message','content':[{'type':'output_text','text':'Claim https://fabricated.example/ is a source.',
             'annotations':[{'type':'url_citation','url':'https://example.org/paper','title':'Paper'},
                            {'type':'url_citation','url':'javascript:alert(1)','title':'Bad'}]}]}]}
        research=p.extract_search(response)
        self.assertEqual([s['url'] for s in research['sources']],['https://example.org/paper'])
        self.assertEqual(research['status'],'searched')
        self.assertEqual(p.extract_search({'output':[]})['status'],'not_performed')

    def test_rejects_unbacked_literature_claim(self):
        for raw in [study('literature_assisted'),study('literature_assisted',['made-up'])]:
            with self.assertRaises(ValueError):p.validate_ablation(raw,self.doc,'a2',self.research)

    def test_retrieved_sources_force_literature_label(self):
        research={'sources':[{'id':'src1','title':'Paper','url':'https://example.org'}]}
        result=p.validate_ablation(study(sources=['src1']),self.doc,'a2',research)
        alt=result['alternatives'][0]
        self.assertEqual(alt['origin'],'literature_assisted')
        self.assertEqual(alt['fork_state'],'s0')
        self.assertFalse(alt['search_cost_measured'])

    def test_rejoin_and_terminal_claims_checked(self):
        raw=study();alt=raw['alternatives'][0]
        alt.update(outcome='rejoined',rejoin_state='s1')
        with self.assertRaises(ValueError):p.validate_ablation(raw,self.doc,'a2',self.research)
        alt['rejoin_state']='s2'
        self.assertEqual(p.validate_ablation(raw,self.doc,'a2',self.research)['alternatives'][0]['rejoin_state'],'s2')
        alt.update(outcome='closed');alt['route'][0]['want']='Still need to prove the theorem'
        with self.assertRaises(ValueError):p.validate_ablation(raw,self.doc,'a2',self.research)
        alt['outcome']='infinite'
        with self.assertRaises(ValueError):p.validate_ablation(raw,self.doc,'a2',self.research)

    def test_full_staged_workflow_without_network(self):
        replies=iter([fixture(),study(),study(),{'steps':['a2'],'rationale':'Factoring matches the target.'}])
        updates=[]
        result=p.run_pipeline(PROOF,4,lambda *_:next(replies),lambda *_:self.research,
                              lambda message,doc:updates.append((message,copy.deepcopy(doc))),lambda:False)
        self.assertEqual(set(result['ablations']),{'a1','a2'})
        self.assertEqual(result['critical']['steps'],['a2'])
        self.assertEqual(result['original_proof'],PROOF)
        self.assertTrue(any(doc and len(doc['ablations'])==1 for _,doc in updates))

    def test_one_bounded_format_correction(self):
        bad=study();bad['alternatives'][0]['route'][0]['want']=None
        replies=iter([fixture(),bad,study(),study(),{'steps':['a2'],'rationale':'Factoring.'}])
        calls=[]
        def ask(instruction,data):
            calls.append((instruction,data));return next(replies)
        result=p.run_pipeline(PROOF,4,ask,lambda *_:self.research,lambda *_:None,lambda:False)
        self.assertEqual(len(calls),5)
        self.assertIn('validation_error',calls[2][1])
        self.assertEqual(len(result['ablations']),2)

    def test_repeated_invalid_result_stops_after_one_correction(self):
        bad=study();bad['alternatives'][0]['route'][0]['want']=None
        replies=iter([fixture(),bad,bad]);calls=[]
        def ask(*_):calls.append(1);return next(replies)
        with self.assertRaises(ValueError):
            p.run_pipeline(PROOF,4,ask,lambda *_:self.research,lambda *_:None,lambda:False)
        self.assertEqual(len(calls),3)

    def test_resume_skips_completed_ablations_and_saved_research(self):
        partial=copy.deepcopy(self.doc)
        partial['ablations']['a1']=p.validate_ablation(study(),partial,'a1',self.research)
        partial['research_records']['a2']=self.research
        replies=iter([study(),{'steps':['a2'],'rationale':'Factor.'}]);calls=[]
        def ask(*_):calls.append(1);return next(replies)
        result=p.run_pipeline(PROOF,4,ask,lambda *_:self.fail('Research should not repeat'),
                              lambda *_:None,lambda:False,partial)
        self.assertEqual(len(calls),2)
        self.assertEqual(set(result['ablations']),{'a1','a2'})
        self.assertNotIn('a2',partial['ablations'])

    def test_stop_prevents_subsequent_calls(self):
        with self.assertRaises(InterruptedError):
            p.run_pipeline(PROOF,4,lambda *_:self.fail('Unexpected API call'),None,lambda *_:None,lambda:True)

    def test_import_rebuilds_graphs_and_marks_provenance(self):
        sample=json.loads((ROOT/'main/explorer/example.json').read_text())
        sample['states']=[{'id':'fake','have':[],'want':[]}]
        imported=p.validate_import(sample)
        self.assertEqual(len(imported['states']),15)
        self.assertTrue(imported['closure'])
        sourced=[s for s in imported['ablations'].values() if s['research']['sources']]
        self.assertEqual(len(sourced),1)
        self.assertIn('Imported provenance',sourced[0]['research']['verification'])
        self.assertIn('2509.00881v1',sourced[0]['research']['sources'][0]['url'])

    def test_import_rejects_unsafe_sources(self):
        self.doc['ablations']['a2']={**study('literature_assisted',['s']),
           'research':{'sources':[{'id':'s','url':'javascript:alert(1)','title':'Bad'}]}}
        with self.assertRaises(ValueError):p.validate_import(self.doc)

    def test_persistence_and_path_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            service=ExplorerService(directory,None,None,lambda:None,'test')
            saved=service.import_document(self.doc)
            other=ExplorerService(directory,None,None,lambda:None,'test')
            self.assertEqual(other.get(saved['id'])['document']['original_proof'],PROOF)
            with self.assertRaises(ValueError):other.get('../../.env')
            job=saved.copy();job.update(status='running');service._save(job)
            third=ExplorerService(directory,None,None,lambda:None,'test')
            self.assertEqual(third.get(job['id'])['status'],'interrupted')

    def test_async_service_uses_real_pipeline_with_injected_transport(self):
        replies=iter([fixture(),study(),study(),{'steps':['a2'],'rationale':'Recognize the factor.'}])
        def call(**_):return json.dumps(next(replies))
        with tempfile.TemporaryDirectory() as directory, patch.dict('os.environ',{'OPENAI_API_KEY':'test-only'}):
            service=ExplorerService(directory,call,None,lambda:None,'test')
            job=service.create({'proof':PROOF,'max_steps':4,'online_search':False})
            for _ in range(100):
                job=service.get(job['id'])
                if job['status']!='running':break
                time.sleep(.01)
            self.assertEqual(job['status'],'complete',job['message'])
            self.assertEqual(len(job['requests']),4)
            self.assertEqual(len(job['document']['ablations']),2)

class ServiceResearchTests(unittest.TestCase):
    def wait(self, service, job):
        for _ in range(200):
            job=service.get(job['id'])
            if job['status']!='running':return job
            time.sleep(.01)
        self.fail('Background test did not finish')

    def test_search_transport_and_source_attribution_end_to_end(self):
        response={'id':'research1','status':'completed','output':[
            {'id':'search1','type':'web_search_call','status':'completed',
             'action':{'type':'search','sources':[{'url':'https://example.org/math','title':'A source'}]}},
            {'type':'message','content':[{'type':'output_text','text':'A source-supported method.','annotations':[]}]}]}
        replies=iter([fixture(),study('literature_assisted',['src1']),study('literature_assisted',['src1']),
                      {'steps':['a2'],'rationale':'Factor recognition.'}])
        from unittest.mock import MagicMock
        transport=MagicMock();transport.__enter__.return_value.read.return_value=json.dumps(response).encode()
        with tempfile.TemporaryDirectory() as directory, patch.dict('os.environ',{'OPENAI_API_KEY':'test-only'}), patch('main.explorer_service.urllib.request.urlopen',return_value=transport) as opened:
            service=ExplorerService(directory,lambda **_:json.dumps(next(replies)),lambda:None,lambda:None,'test')
            job=self.wait(service,service.create({'proof':PROOF,'max_steps':4,'online_search':True}))
            self.assertEqual(job['status'],'complete',job['message'])
            self.assertEqual(opened.call_count,2)
            payload=json.loads(opened.call_args.args[0].data)
            self.assertEqual(payload['tools'],[{'type':'web_search'}])
            self.assertIn('web_search_call.action.sources',payload['include'])
            self.assertFalse(payload['store'])
            doc=job['document'];self.assertEqual(len(doc['research_records']),2)
            self.assertEqual(doc['ablations']['a2']['alternatives'][0]['origin'],'literature_assisted')
            self.assertNotIn('test-only',json.dumps(job))

    def test_search_failure_is_explicit_and_does_not_fabricate_sources(self):
        replies=iter([fixture(),study(),study(),{'steps':['a2'],'rationale':'Factor recognition.'}])
        with tempfile.TemporaryDirectory() as directory, patch.dict('os.environ',{'OPENAI_API_KEY':'test-only'}), patch('main.explorer_service.urllib.request.urlopen',side_effect=OSError('offline')):
            service=ExplorerService(directory,lambda **_:json.dumps(next(replies)),lambda:None,lambda:None,'test')
            job=self.wait(service,service.create({'proof':PROOF,'max_steps':4,'online_search':True}))
            self.assertEqual(job['status'],'complete',job['message'])
            study_data=job['document']['ablations']['a2']
            self.assertEqual(study_data['research']['status'],'unavailable')
            self.assertEqual(study_data['research']['sources'],[])
            self.assertFalse(study_data['alternatives'][0]['research_exposed'])

    def test_stop_during_first_request_keeps_completed_decomposition(self):
        entered=threading.Event();release=threading.Event();calls=[]
        def call(**_):
            calls.append(1);entered.set();release.wait(2);return json.dumps(fixture())
        with tempfile.TemporaryDirectory() as directory, patch.dict('os.environ',{'OPENAI_API_KEY':'test-only'}):
            service=ExplorerService(directory,call,None,lambda:None,'test')
            job=service.create({'proof':PROOF,'online_search':False})
            self.assertTrue(entered.wait(2));service.stop(job['id']);release.set()
            job=self.wait(service,job)
            self.assertEqual(job['status'],'stopped');self.assertEqual(len(calls),1)
            self.assertEqual(job['document']['original_proof'],PROOF)

    def test_no_independent_discovery_claim_after_research_exposure(self):
        doc=p.derive_document(fixture(),PROOF)
        research={'sources':[{'id':'src1','title':'Paper','url':'https://example.org'}]}
        result=p.validate_ablation(study(),doc,'a2',research)
        self.assertTrue(result['alternatives'][0]['research_exposed'])

if __name__=='__main__':unittest.main()
