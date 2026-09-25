import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
agent=load('a',ROOT/'main/agent_server.py')
viewer=load('v',ROOT/'tools/visualize_control_vs_rag_results.py')
class Tests(unittest.TestCase):
 def test_canonical_name_ignores_model_label(self):
  graph={'nodes':[{'id':'n','label':'Exact library name'}],'edges':[]}
  replies=iter([{'highlights':[{'quote':'A proof.','kind':'library','node_id':'n','strategy':'Invented alias','annotation':'Explanation.'}]}, {'edits':[{'id':'p1','action':'keep','replacement':'A proof.','reason':'Required.'}]}, {'edits':[]}])
  with patch.object(agent,'load_graph',return_value=graph):
   out=agent.run_library_pipeline('Prove', 'A proof.', lambda _:json.dumps(next(replies)))
  self.assertEqual(out['annotated_control']['highlights'][0]['strategy'],'Exact library name')
  self.assertEqual(out['library_graph'],graph)
  self.assertNotIn('Invented alias',out['comparison_html'])
 def test_library_label_not_required_from_model(self):
  graph={'nodes':[{'id':'n','label':'Exact library name'}],'edges':[]}
  replies=iter([{'highlights':[{'quote':'A proof.','kind':'library','node_id':'n','annotation':'Explanation.'}]}, {'edits':[{'id':'p1','action':'keep','replacement':'A proof.','reason':'Required.'}]}, {'edits':[]}])
  with patch.object(agent,'load_graph',return_value=graph):
   out=agent.run_library_pipeline('Prove', 'A proof.', lambda _:json.dumps(next(replies)))
  self.assertEqual(out['annotated_control']['highlights'][0]['strategy'],'Exact library name')
 def test_old_records_canonicalized_without_mutation(self):
  raw={'library_graph':{'nodes':[{'id':'n','label':'Canonical'}],'edges':[]},'annotated_control':{'highlights':[{'kind':'library','node_id':'n','strategy':'Alias'}]}}
  out=viewer.canonical_output(raw)
  self.assertEqual(out['annotated_control']['highlights'][0]['strategy'],'Canonical')
  self.assertEqual(raw['annotated_control']['highlights'][0]['strategy'],'Alias')
 def test_unknown_id_rejected(self):
  with self.assertRaises(ValueError):viewer.canonical_output({'library_graph':{'nodes':[]},'annotated_control':{'highlights':[{'kind':'library','node_id':'missing'}]}})
 def test_link_encoding(self):
  link=viewer.graph_reference_link('a/b # c')
  self.assertEqual(unquote(link.split('=',1)[1]),'a/b # c')
 def test_graph_serialization_order_and_safe_text(self):
  out={'input_id':'x','name':'</script><script>bad()</script>','library_graph':{'nodes':[{'id':'n','label':'Canonical','level':1}],'edges':[]},'annotated_control':{'highlights':[
   {'id':'p3','start':4,'kind':'library','node_id':'n','strategy':'Alias','annotation':'again'},
   {'id':'p1','start':0,'kind':'library','node_id':'n','strategy':'Alias','annotation':'first'},
   {'id':'p2','start':2,'kind':'new','strategy':'New method','annotation':'novel'}]}}
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'graph.html';viewer.write_graph_reference_page([out],p);s=p.read_text()
  payload=s.split('<script id="proof-reference-data" type="application/json">')[1].split('</script>')[0]
  data=json.loads(payload);steps=data['proofs']['x']['steps']
  self.assertEqual([x['id'] for x in steps],['p1','p2','p3'])
  self.assertEqual(steps[0]['label'],'Canonical')
  self.assertEqual(steps[2]['node_id'],'n')
  self.assertNotIn('</script>',payload)
if __name__=='__main__':unittest.main()
