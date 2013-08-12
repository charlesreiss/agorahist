import sqlite3

def connect():
  conn = sqlite3.connect(filename)
  conn.execute('''PRAGMA foreign_keys = ON''')
  return conn

def _date(x):
  if x == None:
    return None
  else:
    return x.isoformat()

def _insert_category(conn, record, source_name):
  conn.execute('''
    INSERT OR REPLACE INTO category (name, description)
    VALUES (:name, :description)
  ''', {'name': record['name'], 'description': record['description']})

def _insert_history(conn, rule_id, record, source_name):
  conn.execute('''
    INSERT OR REPLACE INTO rule_history (
      rule_id, text, history_date, revision,
      proposal
    ) VALUES (
      :rule_id, :text, :date, :revision,
      :proposal
    )
  ''', {'rule_id': rule_id, 'text': record.get('text'),
        'date': _date(record.get('date')),
        'revision': record.get('revision'),
        'proposal': record.get('proposal')})
  row_id = conn.lastrowid
  conn.execute('''
    INSERT OR IGNORE INTO history_sources (
      rule_history_id, source_name
    ) VALUES (:row_id, :source_name)
  ''', {'row_id': row_id, 'source_name': source_name})

def _insert_annotation(conn, rule_id, record, category, source_name):
  conn.execute('''
    INSERT OR REPLACE INTO rule_annotations (
      rule_id, text, cfj_ids, cfj_date, category
    ) VALUES (
      :rule_id,
      :text,
      :cfj_ids,
      COALESCE(SELECT cfj_date FROM rule_annotations WHERE text = :text,
               :cfj_date),
      COALESCE(SELECT category FROM rule_annotations WHERE text = :text,
               :category)
    )
  ''', {
    'rule_id': rule_id,
    'text': record['text'],
    'cfj_id': record.get('cfj'),
    'cfj_date': record.get('cfj_date'),
    'category': category,
  })
  row_id = conn.lastrowid
  conn.execute('''
    INSERT OR IGNORE INTO annotation_sources ( annotation_id, source_name)
    VALUES ( :row_id, :source_name )
  ''', {'row_id': row_id, 'source_name': source_name})


def _insert_rule(conn, record, source_name):
  replacements = {
      'rule_id': record['id'],
      'category_name': record.get('category'),
      'text': record['text'],
      'title': record.get('title'),
      'revision': record.get('revision'),
      'revision_date': record.get('revision_date')
  }

  conn.execute('''
    INSERT OR REPLACE INTO rules (rule_id, category_name) VALUES (
      :rule_id,
      COALESCE(SELECT category_name FROM rules WHERE rule_id = :rule_id,
               :category_name)
    )
  ''', replacements)

  if record['text'] != None:
    conn.execute('''
      INSERT OR REPLACE INTO rule_texts (
        rule_id, text, title, revision, revision_date
      ) VALUES (
        :rule_id,
        COALESCE(:title,
                 SELECT title FROM rule_texts WHERE rule_id = :rule_id
                 AND revision = :revision AND revision IS NOT NULL),
        :text,
        :revision,
        COALESCE(:revision_date,
                 SELECT revision_date FROM rule_texts WHERE rule_id = :rule_id
                 AND revision = :revision AND revision IS NOT NULL)
      )
    ''', replacements)
    row_id = conn.lastrowid

    conn.execute('''
      INSERT OR IGNORE INTO text_sources (text_id, source_name)
      VALUES (:row_id, :source_name)
    ''', {'row_id': row_id, 'source_name': source_name})

  if 'history' in record:
    for history_entry in record['history']:
      _insert_history(conn, rule['id'], history_entry)
 
  if 'annotation' in record:
    for annotation_entry in record['annotation']:
      _insert_annotation(conn, rule['id'], record.get('category'),
                         annotation_entry)


def insert_record(conn, record, source_name):
  if record['type'] == 'rule':
    _insert_rule(conn, record, source_name)
  elif record['type'] == 'category':
    _insert_category(conn, record, source_name)
  elif record['type'] == 'annotation':
    _insert_annotation(conn, record, source_name)
