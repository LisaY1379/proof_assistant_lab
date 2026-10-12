"""Load the published project protocol and check its annotation contract.

These checks enforce complete records and references, not mathematical truth.
"""
import copy
import hashlib
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ('tools/proof_explorer/protocol-reference.html', 'tools/proof_explorer/protocol.html')


class ProtocolText(HTMLParser):
    def __init__(self, attribute, value):
        super().__init__()
        self.attribute, self.value = attribute, value
        self.depth, self.parts = 0, []

    def handle_starttag(self, tag, attrs):
        if dict(attrs).get(self.attribute) == self.value and not self.depth:
            self.depth = 1
        elif self.depth and tag not in {'br', 'hr', 'input', 'meta', 'link', 'img'}:
            self.depth += 1
        if self.depth:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if self.depth:
            self.depth -= 1
            self.parts.append('\n')

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)


def load_protocol():
    parts = []
    for path, selector in zip(SOURCES, [('id', 'protocol-content'), ('class', 'tour-bottom')]):
        parser = ProtocolText(*selector)
        parser.feed((ROOT / path).read_text(encoding='utf-8'))
        content = '\n'.join(line.strip() for line in ''.join(parser.parts).splitlines() if line.strip())
        if len(content) < 500:
            raise ValueError(f'Project protocol content is missing in {path}')
        parts.append(content)
    content = '\n\n'.join(parts)
    return {'version': '0.1', 'sources': list(SOURCES),
            'sha256': hashlib.sha256(content.encode()).hexdigest(), 'text': content}


CONTRACT = '''
Follow the project protocol below, including its priority rule: basic first; when
basic moves leave a local gap, state the gap, make an observation, select a move,
verify it, and resume basic reasoning. Do not fabricate trials or historical thoughts.
A familiar theorem or one-line factorization is not automatically a basic step.
An observation motivates a choice; it is never an extra established fact.

In addition to the graph schema, output:
"protocol": {"version":"0.1", "context": {
  "domains":"domains, quantifiers, and initial assumptions",
  "definitions":"definitions used", "basic_rules":"declared B-D/B-C/B-L rules and named extensions",
  "toolkit":[{"id":"t1","name":"...","statement":"exact result used","hypotheses":"required hypotheses"}]
}}
Every grouped step must contain a "protocol" record:
{"direction":"forward|backward|meeting|exploratory",
 "context":"facts, domains, and scoped assumptions BEFORE this move",
 "target":"current goal", "basic_progress":"basic moves that address it, with their rules",
 "remaining_gap":"local gap requiring selection, or none with explanation",
 "observation":{"target_feature":"...","available_feature":"...","connection":"..."},
 "actions":[{"id":"u1","kind":"B-D|B-C|B-L|strategic|unresolved",
   "role":"execution or selected strategic role (representation, planning, construction, method, cases)",
   "move":"specific action", "provenance":"given, earlier action, or motivating observation",
   "rule":"explicit permitted rule, or why selection exceeds the basic rules",
   "inputs":"specific facts and locally available inputs",
   "toolkit_uses":[{"id":"t1","hypotheses_check":"check every hypothesis here"}],
   "verification":"calculation/inference; for strategic actions describe what must be checked",
   "verifies":[]}],
 "relation":{"kind":"deduction|equivalent|sufficient|AND|OR|cases|scoped|meeting|unresolved",
   "justification":"exact implication or equivalence and required branches",
   "side_conditions":"domains, parameter ranges, quantifiers, and discharged assumptions; or none with reason"},
 "remaining_obligations":"all remaining obligations after the move; explicitly say none if closed"}

Keep grouped source quotes nonoverlapping, but split choice and execution into ordered
atomic actions inside each step. Action IDs are local u1,u2,... . Each strategic action
must be checked by a LATER B-D/B-C/B-L action whose verifies array names that choice.
Basic verification does not retroactively make selection basic. Execution may cite
an earlier local action's result through inputs; never use a future result.
Use unresolved when context or justification is missing, rather than inventing certainty.
An unresolved group is exploratory: it may open goals but must not add established
facts or close goals. Keep failed/exploratory proposals outside the proof's support.

For goal replacement, record equivalent, sufficient, AND, OR, cases, or scoped;
all opens entries in the state graph are REQUIRED obligations. For an OR reduction,
choose one sufficient route and open only its required obligations, not every candidate.
The current graph has a global fact list: encode conditional or quantified propositions
as complete statements; never promote a local assumption/witness into a global fact.
Record scoped reasoning and discharge in the atomic actions. If this cannot be
represented faithfully, keep the obligation open and mark the group unresolved.
A meeting must match facts to goals with the same assumptions and side conditions.
The step budget limits GROUPS, not the choice/verification records inside each group.

PROJECT PROTOCOL (authoritative project instructions):
'''


def validate_protocol(raw, steps, required=False):
    supplied = raw.get('protocol')
    if supplied is None and not required:
        if any('protocol' in step for step in steps):
            raise ValueError('Step protocol records require a declared protocol context')
        return None

    def mapping(value, name):
        if not isinstance(value, dict):
            raise ValueError(f'{name} must be an object')
        return value

    def words(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'{name} must be nonempty text')

    def items(value, name, limit=100):
        if not isinstance(value, list) or len(value) > limit:
            raise ValueError(f'{name} must be a list of at most {limit} items')
        return value

    protocol = copy.deepcopy(mapping(supplied, 'protocol'))
    if protocol.get('version') != '0.1':
        raise ValueError('protocol.version must be 0.1')
    context = mapping(protocol.get('context'), 'protocol.context')
    for key in ('domains', 'definitions', 'basic_rules'):
        words(context.get(key), f'protocol.context.{key}')
    toolkit = set()
    for result in items(context.get('toolkit'), 'protocol.context.toolkit'):
        mapping(result, 'toolkit result')
        for key in ('id', 'name', 'statement', 'hypotheses'):
            words(result.get(key), f'toolkit.{key}')
        if result['id'] in toolkit:
            raise ValueError('Duplicate toolkit ID')
        toolkit.add(result['id'])
    for step in steps:
        label = step['id'] + '.protocol'
        record = mapping(step.get('protocol'), label)
        for key in ('context', 'target', 'basic_progress', 'remaining_gap', 'remaining_obligations'):
            words(record.get(key), f'{label}.{key}')
        if record.get('direction') not in {'forward', 'backward', 'meeting', 'exploratory'}:
            raise ValueError(f'{label}: invalid direction')
        observation = mapping(record.get('observation'), label + '.observation')
        for key in ('target_feature', 'available_feature', 'connection'):
            words(observation.get(key), f'{label}.observation.{key}')
        relation = mapping(record.get('relation'), label + '.relation')
        if relation.get('kind') not in {'deduction', 'equivalent', 'sufficient', 'AND', 'OR', 'cases', 'scoped', 'meeting', 'unresolved'}:
            raise ValueError(f'{label}: invalid goal relation')
        for key in ('justification', 'side_conditions'):
            words(relation.get(key), f'{label}.relation.{key}')
        actions = items(record.get('actions'), label + '.actions', 80)
        if not actions:
            raise ValueError(f'{label}: record basic execution or strategic choice explicitly')
        choices, verified = set(), set()
        unresolved = relation['kind'] == 'unresolved'
        for i, action in enumerate(actions):
            mapping(action, 'protocol action')
            if action.get('id') != f'u{i+1}':
                raise ValueError(f'{label}: atomic IDs must be u1, u2, ...')
            kind = action.get('kind')
            if kind not in {'B-D', 'B-C', 'B-L', 'strategic', 'unresolved'}:
                raise ValueError(f'{label}: invalid basic/strategic classification')
            for key in ('role', 'move', 'provenance', 'rule', 'inputs', 'verification'):
                words(action.get(key), f'{label}.actions.{key}')
            for use in items(action.get('toolkit_uses'), 'toolkit_uses'):
                mapping(use, 'toolkit use')
                if not isinstance(use.get('id'), str) or use['id'] not in toolkit:
                    raise ValueError(f'{label}: unknown toolkit dependency')
                words(use.get('hypotheses_check'), 'toolkit hypotheses_check')
            checks = items(action.get('verifies'), 'verifies')
            if any(not isinstance(ref, str) or ref not in choices for ref in checks):
                raise ValueError(f'{label}: verification must reference an earlier strategic choice')
            if checks and kind not in {'B-D', 'B-C', 'B-L'}:
                raise ValueError(f'{label}: choices require separate basic verification actions')
            verified.update(checks)
            if kind == 'strategic':
                choices.add(action['id'])
            unresolved |= kind == 'unresolved'
        if choices - verified and not unresolved:
            raise ValueError(f'{label}: strategic choice lacks a later verification action')
        if unresolved:
            if step['adds'] or step['closes'] or record['direction'] != 'exploratory':
                raise ValueError(f'{label}: unresolved reasoning cannot establish facts or close goals')
        elif step['closes']:
            if step['opens']:
                if record['direction'] != 'backward' or relation['kind'] not in {'equivalent', 'sufficient', 'AND', 'OR', 'cases', 'scoped'}:
                    raise ValueError(f'{label}: goal replacement needs a backward logical relation')
            elif record['direction'] != 'meeting' or relation['kind'] != 'meeting':
                raise ValueError(f'{label}: goal discharge needs a meeting record')
        elif record['direction'] == 'meeting' or relation['kind'] == 'meeting':
            raise ValueError(f'{label}: meeting must discharge a goal')
    protocol['validation'] = 'Annotation structure checked; classifications and mathematics require review.'
    return protocol
