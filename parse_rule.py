import datetime
import logging
import re

def _unindent(text):
  lines = text.split('\n')
  if lines[-1] == '':
    lines = lines[:-1]
  nonempty_lines = filter(lambda x: re.match(r'^\s*$', x) == None, lines)
  if len(nonempty_lines) == 0:
    return u''
  indents = map(lambda x: re.search(r'^\s*', x).end(), nonempty_lines)
  min_indent = min(indents)
  lines = map(lambda x: x[min_indent:], lines)
  return '\n'.join(lines) + '\n'

def _lines(text):
  result = []
  cur_line = None
  for line in text.split('\n'):
    if line == '':
      continue
    if (cur_line != None and
        cur_line.count('\n') == 0 and
        cur_line.count('(') > cur_line.count(')')):
      cur_line += '\n' + line
    elif cur_line != None and line.startswith(' '):
      cur_line += '\n' + line
    else:
      if cur_line != None:
        result.append(cur_line)
      cur_line = line
  if cur_line != None:
    result.append(cur_line)
  return result


def _norm_whitespace(text):
  text = re.sub(r'\s+', ' ', text)
  text = re.sub(r'^\s+|\s+$', '', text)
  return text

def _parse_date(raw_date):
  if raw_date == None:
    return None
  raw_date = raw_date.replace('ca. ', '')
  raw_date = raw_date.replace('Jaun', 'Jan')
  raw_date = raw_date.replace('Febraury', 'February')
  raw_date = raw_date.replace('Apirl', 'April')
  raw_date = raw_date.replace('Augut', 'August')
  raw_date = raw_date.replace('.', '')
  raw_date = raw_date.replace(',', '')
  raw_date = raw_date.replace('<ay', 'May')
  raw_date = raw_date.replace(' 010', ' 2010')
  raw_date = raw_date.replace(' 011', ' 2011')
  raw_date = raw_date.replace(' 012', ' 2012')
  raw_date = raw_date.replace(' 013', ' 2013')
  raw_date = _norm_whitespace(raw_date)
  if re.match(r'^[a-zA-Z]+ \d+$', raw_date) != None:
    try:
      parsed_date = datetime.datetime.strptime(raw_date, '%B %Y')
    except ValueError:
      parsed_date = datetime.datetime.strptime(raw_date, '%b %Y')
  elif re.match(r'^[a-zA-Z]+ or [a-zA-Z]+ \d+$', raw_date) != None:
    m = re.match(r'^[a-zA-Z]+ or ([a-zA-Z]+ \d+)$', raw_date)
    raw_date = m.group(1)
    try:
      parsed_date = datetime.datetime.strptime(raw_date, '%B %Y')
    except ValueError:
      parsed_date = datetime.datetime.strptime(raw_date, '%b %Y')
  elif re.search(r'^[A-Z]', raw_date) != None:
    try:
      parsed_date = datetime.datetime.strptime(raw_date, '%B %d %Y')
    except ValueError:
      try: 
        parsed_date = datetime.datetime.strptime(raw_date, '%b %d %Y')
      except ValueError:
        logging.error('Error parsing date <%s>', raw_date)
        raise
  else:
    try:
      parsed_date = datetime.datetime.strptime(raw_date, '%d %B %Y')
    except ValueError:
      try:
        parsed_date = datetime.datetime.strptime(raw_date, '%d %b %Y') 
      except ValueError:
        logging.error('Error parsing date <%s>', raw_date)
        raise
  return datetime.date(parsed_date.year, parsed_date.month,
      parsed_date.day)

def _parse_history_line(text):
  text = _norm_whitespace(text)
  logging.debug('history line: %s', text)
  result = {}
  m = re.search(r'(?s)(, su[bs][^,]*|, co[sm][^,]*|\(\S+\))$', text)
  post_text = ''
  if m != None:
    post_text = m.group(0)
    text = text[:m.start()]
  m = re.match(r'(?s)(?P<text>.*), (?P<date>[^,]+)$', text)
  if m != None:
    result['text'] = _norm_whitespace(m.group('text') + post_text)
    try:
      result['date'] = _parse_date(m.group('date'))
    except ValueError:
      logging.error('Parsing <%s> (text %s; date %s; post-text %s): %s', 
          text, m.group('text'), m.group('date'), post_text)
      raise
  else:
    result['text'] = text + post_text
    date = None
  m = re.search(r'Proposal ([\d_\-\[\]]+)', text)
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

  if text.startswith('Repeal'):
    result['repeal'] = True
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
        if 'date' in history[-1]:
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

def _parse_annotations(text):
  annotations = []
  LINES_NOCFJ = r'\s*[^&\s].*(?:\n(?!.CFJ)(?!\[).*)*'
  CFJ_CALLED = r'\s*(?:\([cC]alled\s+(?P<called>[^)]+)\))?\s*'
  CFJ_JUDGED = r'\s*(?:\(?[jJ]udged\s+(?:TRUE|FALSE)?,?\s*' + \
               r'(?P<judged>\S+ \d+,? \d+)(?:[^)]*\))?)?\s*'
  OPT_PARENS = r'(?:\([^)]+\))?'
  CFJ_IDS = r'CFJs? ' + \
            r'(?P<id>\d+[abcde]?|\?\?\?)(?:-(?P<id_end>\d+)|\s*' + \
            OPT_PARENS + r'\s*\&\s*(?:CFJ\s*)?(?P<id2>\d+[abcde]?))?' + \
            r'(?!\s*is)(?!\s*were)(?!\d)'
  for m in re.finditer(
      CFJ_IDS + r'[:,]?' + CFJ_CALLED + CFJ_JUDGED + r':?(?P<text>' + 
      LINES_NOCFJ + r')', text):
    ids = m.group('id')
    if ids == '???':
      ids = None
    elif m.group('id2') != None:
      ids += ',' + m.group('id2')
    elif m.group('id_end') != None:
      low_id = int(ids)
      ids = ','.join(map(str,range(low_id, int(m.group('id_end')) + 1)))
    text = _norm_whitespace(m.group('text'))
    if text.endswith(']'):
      text = text[:-1]
    if text.endswith('"') and text.startswith('"'):
      text = text[1:-1]
    annotation = {
      'cfj': ids,
      'date': _parse_date(m.group('called')),
      'judged_date': _parse_date(m.group('judged')),
      'text': text,
    }
    if annotation['date'] == None:
      del annotation['date']
    if annotation['judged_date'] == None:
      del annotation['judged_date']
    if annotation['cfj'] == None:
      del annotation['cfj']
    annotations.append(annotation)
  annotations = sorted(annotations,
      key=lambda x: \
          -1 if 'cfj' not in x else int(re.match('^(\d+)', x['cfj']).group(1)),
  )
  return annotations

def parse_rule_flr(text):
  result = {}
  m = re.search(
      r'^Rule (?P<id>\d+)(?:/(?P<revision>\d+))? \((?P<pow_note>[^)]+)\)\s*' +
      r'(?:\[[^\n]+\]\s*)?\n' +
      r'(?P<title>.*)',
      text)
  if m != None:
    result['title'] = _norm_whitespace(m.group('title'))
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
    if not (text.startswith('THE FULL LOGICAL') or
            text.startswith('Rule N') or
            text.startswith('Rule n') or
            text.startswith('Index of ') or
            text.startswith('Statist') or
            text.startswith('[Rules are listed') or
            re.search(r'^\s*\[Last proposal', text) != None or
            text.startswith('END OF THE') or
            re.search('^\s*END OF THE', text) != None or
            text.startswith('Miscellaneous') or
            text.startswith('Contracts /') or
            text.startswith('Truthfulness') or
            text.startswith('Rules are listed as follows')):
      logging.error('Non-rule {{%s}}', text)
    return None
  text = re.sub(r'^\s*\n', '', text)
  content = None
  history = None
  annotations = []
  if text.startswith(' ') or text.startswith('History:'):
    m = re.search(r'^((?: .*\n|\n)*)', text)
    content = _unindent(m.group(1))
    text = text[m.end():]
    m = re.search(r'(?:\n|^)History:\s*((?:\n.*\S.*)+)', text)
    if m != None:
      history_text = _lines(m.group(1))
      # TODO(Charles): Find continued lines
      history_text = filter(lambda x: re.match('^\s*$', x) == None,
          history_text)
      logging.debug('history lines: %s', history_text)
      try:
        history = map(_parse_history_line, history_text)
      except ValueError:
        logging.error('Error parsing <%s>', history_text)
        raise
      last_revision = None
      for entry in history:
        if 'revision' not in entry and last_revision != None:
          entry['after_revision'] = last_revision
        elif 'revision' in entry:
          last_revision = entry.get('revision')
      if len(history) > 0 and 'repeal' in history[-1]:
        result['repealed'] = True
      text = text[:m.start()] + '\n\n\n' + text[m.end():]
    else:
      logging.error('Could not find history in %s', text)
    annotations = _parse_annotations(text)
  else:
    # TODO(Charles): Find CFJ annotations.
    content = text
  result['text'] = re.sub(r'\n\n$', '\n', content)
  if history != None:
    result['history'] = history
  if len(annotations) > 0:
    result['annotations'] = annotations
  return result

SEP = '----------------------------------------------------------------------'
CAT_SEP = \
    '======================================================================'

def parse_flr(flr_stream, callback):
  current_segment = ''
  current_category = None
  for line in flr_stream:
    if re.match(r'^-{40,}$', line) != None:
      m = re.search(r'(?s)={40,}\n(?P<name>[^\n]*)\n(?P<description>.*)',
          current_segment)
      if m != None:
        current_category = _norm_whitespace(m.group('name'))
        if not current_category.startswith('Table of Content'):
          callback({
            'type': 'category',
            'name': current_category,
            'description': _norm_whitespace(m.group('description'))
            })
      else:
        current_segment = re.sub(r'^\s+','',current_segment)
        result = parse_rule_flr(current_segment)
        if result != None:
          result['type'] = 'rule'
          result['category'] = current_category
          callback(result)
        else:
          m = re.search(r'^\s*(\S.*)\n', current_segment)
          if m != None:
            sub_category = m.group(1)
          else:
            logging.error('No subcategory for %s', current_segment)
            sub_category = None
          for annotation in  _parse_annotations(current_segment):
            annotation['type'] = 'annotation'
            annotation['category'] = current_category
            annotation['subcategory'] = sub_category
            callback(annotation)
      current_segment = ''
    else:
      current_segment += line
  if re.match(r'^\s*$', current_segment) == None:
    logging.warning('Extra segment: %s', current_segment)

def parse_zefram(zefram_stream, callback):
  current_segment = ''
  for line in zefram_stream:
    if re.match(r'^-{40,}$', line) != None:
      results = parse_rule_zefram(current_segment)
      if results != None:
        for item in results:
          item['type'] = 'rule'
          callback(item)
      current_segment = ''
    else:
      current_segment = current_segment + line 
