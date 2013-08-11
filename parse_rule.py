import datetime
import logging
import re

def _unindent(text):
  lines = text.split('\n')
  if lines[-1] == '':
    lines = lines[:-1]
  nonempty_lines = filter(lambda x: re.match(r'^\s*$', x) == None, lines)
  indents = map(lambda x: re.search(r'^\s*', x).end(), nonempty_lines)
  min_indent = min(indents)
  lines = map(lambda x: x[min_indent:], lines)
  return '\n'.join(lines) + '\n'

def _parse_date(raw_date):
  if raw_date == None:
    return None
  raw_date = raw_date.replace('Jaun', 'Jan')
  raw_date = raw_date.replace('Febraury', 'February')
  raw_date = raw_date.replace('Apirl', 'April')
  raw_date = raw_date.replace('Augut', 'August')
  raw_date = raw_date.replace('.', '')
  if re.match(r'^[a-zA-Z]+ \d+$', raw_date) != None:
    try:
      parsed_date = datetime.datetime.strptime(raw_date, '%B %Y')
    except ValueError:
      parsed_date = datetime.datetime.strptime(raw_date, '%b %Y')
  elif re.search(r'^[A-Z]', raw_date) is not None:
    parsed_date = datetime.datetime.strptime(raw_date, '%b %d %Y')
  else:
    try:
      parsed_date = datetime.datetime.strptime(raw_date, '%d %B %Y')
    except ValueError:
      parsed_date = datetime.datetime.strptime(raw_date, '%d %b %Y') 
  return datetime.date(parsed_date.year, parsed_date.month,
      parsed_date.day)

def _parse_history_line(text):
  result = {}
  m = re.search(r'(, substantial)$', text)
  post_text = ''
  if m != None:
    post_text = m.group(0)
    text = text[:m.start()]
  m = re.match(r'(?P<text>.*), (?P<date>[^,]+)', text)
  if m != None:
    result['text'] = m.group('text') + post_text
    result['date'] = _parse_date(m.group('date'))
  else:
    result['text'] = text + post_text
    date = None
  m = re.search(r'Proposal (\d+)', text)
  if m != None:
    result['proposal'] = m.group(1)
  m = re.search(r'Proposal "([^"]+)"', text)
  if m != None:
    result['proposal'] = m.group(1)
  m = re.search(r'\(([.\d]+)\)', text)
  if m != None:
    result['revision'] = m.group(1)
  elif (text.startswith('Created') or text.startswith('Enacted') or
        text.startswith('Initial')):
    result['revision'] = u'0'
  logging.debug('Parsing [%s] as [%s]', text, result)
  return result

# Returns (history w/o text, rule texts w/o history)
def parse_rule_zefram(text):
  rule_texts = []
  history = []
  # There may be multiple IDs on this line.
  m = re.match('^\s*RULE (\d+)', text)
  if m != None:
    rule_id = m.group(1)
  else:
    return None
  last_revision = None
  last_date = None
  for m in re.finditer(r'history: (?P<history_text>.*)|' + 
                       r'text:\n\n(?P<rule_text>(?:\n|\s.*\n)+)', text):
    if m.group('history_text') != None:
      last_revision = None
      if m.group('history_text') != '...':
        history.append(_parse_history_line(m.group(1)))
        if 'revision' in history[-1]:
          last_revision = history[-1]['revision']
          last_date = history[-1]['date']
    if m.group('rule_text') != None:
      rule_texts.append(
          {'text': _unindent(m.group('rule_text')),
           'revision': last_revision,
           'date': last_date,
           'id': rule_id,
           })
      if last_revision == None:
        del rule_texts[-1]['revision']
      if last_date == None:
        del rule_texts[-1]['date']
  return [{'history': history, 'id': rule_id}] + rule_texts

def parse_rule_flr(text):
  result = {}
  m = re.search(
      r'^Rule (?P<id>\d+)/(?P<revision>\d+) \((?P<pow_note>[^)]+)\)\n' +
      r'(?P<title>.*)',
      text)
  if m != None:
    result['title'] = m.group('title')
    result['id'] = m.group('id')
    result['revision'] = m.group('revision')
    pow_note = m.group('pow_note')
    text = text[m.end():]
    m = re.match(r'Power=(\d+)', pow_note)
    if m != None:
      result['power'] = m.group(1)
    else:
      logging.error('Could not parse Power annotation: %s', pow_note)
  else:
    return None
  text = re.sub(r'^\s*\n', '', text)
  content = None
  history = None
  annotations = []
  if text.startswith(' '):
    m = re.search(r'^((?: .*\n|\n)+)', text)
    assert(m != None)
    content = _unindent(m.group(1))
    text = text[m.end():]
    m = re.search(r'(?:\n|^)History:\s*\n', text)
    if m != None:
      history_text = text[m.end():].split('\n')
      # TODO(Charles): Find continued lines
      history_text = filter(lambda x: re.match('^\s*$', x) == None,
          history_text)
      logging.debug('history lines: %s', history_text)
      history = map(_parse_history_line, history_text)
      text = text[:m.start()]
    else:
      logging.error('Could not find history in %s', text)
    BRACKETS = r'(?:[^\[\]]+|\[[^\[\]]+\])+'
    for m in re.finditer(r'\[CFJ (?P<id>\d+)(?: \(called (?P<date>[^)]+)\))?: ' +
        r'(?P<text>' + BRACKETS + r')', text):
      annotation = {
        'cfj': m.group('id'),
        'date': _parse_date(m.group('date')),
        'text': re.sub(r'\s+', ' ', m.group('text')),
      }
      if annotation['date'] == None:
        del annotation['date']
      annotations.append(annotation)
  else:
    # TODO(Charles): Find CFJ annotations.
    content = text
  result['text'] = re.sub(r'\n\n$', '\n', content)
  if history != None:
    result['history'] = history
  if len(annotations) >0:
    result['annotations'] = annotations
  return result
