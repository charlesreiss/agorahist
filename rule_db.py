import logging
import sqlite3

def connect(filename, fast_import=False):
  conn = sqlite3.connect(filename, isolation_level='IMMEDIATE')

  conn.text_factory = lambda x: unicode(x, "utf-8", "replace")
  conn.execute('''PRAGMA foreign_keys = ON''')
  conn.execute('''PRAGMA defer_foreign_keys = ON''')
  conn.execute('''PRAGMA fullsync = OFF''')
  if fast_import:
    conn.execute('''PRAGMA journal_mode = OFF''')
    conn.execute('''PRAGMA locking_mode = EXCLUSIVE''')
    conn.execute('''PRAGMA synchronous = OFF''')
  return conn

def _date(x):
  if x == None:
    return None
  else:
    return x.isoformat()

def _insert_category(cursor, record, source_name):
  cursor.execute('''
    INSERT OR REPLACE INTO rule_categories (name, description)
    VALUES (:name, :description)
  ''', {'name': record['name'], 'description': record['description']})

def _get_id(cursor, query, params):
  cursor.execute(query, params)
  result = cursor.fetchone()
  if result == None:
    return None
  else:
    return result[0]

def _insert_history(cursor, rule_id, record, source_name):
  replacements = {
        'rule_id': rule_id,
        'text': record.get('text'),
        'date': _date(record.get('date')),
        'revision': record.get('revision'),
        'after_revision': record.get('after_revision'),
        'proposal': record.get('proposal'),
  }
  replacements['history_id'] = _get_id(cursor, '''
    SELECT rule_history_id FROM rule_history
    WHERE rule_id = :rule_id AND text = :text
    AND (revision = :revision OR (revision IS NULL AND :revision IS NULL))
    LIMIT 1
  ''', replacements)
  cursor.execute('''
    INSERT OR REPLACE INTO rule_history (
      rule_history_id, rule_id, text, history_date, revision, proposal,
      after_revision
    ) VALUES (
      :history_id,
      :rule_id, :text, :date, :revision, :proposal, :after_revision
    )
  ''', replacements)
  row_id = cursor.lastrowid
  cursor.execute('''
    INSERT OR IGNORE INTO history_sources (
      rule_history_id, source_name
    ) VALUES (:row_id, :source_name)
  ''', {'row_id': row_id, 'source_name': source_name})

def _insert_annotation(cursor, rule_id, record, category, source_name):
  replacements = {
    'rule_id': rule_id,
    'text': record['text'],
    'cfj_ids': record.get('cfj'),
    'cfj_date': record.get('cfj_date'),
    'category': category,
  }
  replacements['annotation_id'] = _get_id(cursor, '''
       -- matches UNIQUE constraint
       SELECT annotation_id FROM annotations
       WHERE (rule_id = :rule_id OR (rule_id IS NULL and :rule_id IS NULL))
       AND text = :text
       AND (cfj_ids = :cfj_ids OR (cfj_ids IS NULL and :cfj_ids IS NULL))
       LIMIT 1
  ''', replacements)
  if replacements['annotation_id'] == None:
    logging.info('Inserting annotation for CFJ %s', replacements['cfj_ids'])
  cursor.execute('''
    INSERT OR REPLACE INTO annotations (
      annotation_id, rule_id, text, cfj_ids, cfj_date, category
    ) VALUES (
      :annotation_id,
      :rule_id,
      :text,
      :cfj_ids,
      COALESCE(:cfj_date,
               (SELECT cfj_date FROM annotations WHERE
                annotation_id = :annotation_id)),
      COALESCE(:category,
               (SELECT category FROM annotations WHERE
                annotation_id = :annotation_id))
    )
  ''', replacements)
  row_id = cursor.lastrowid
  cursor.execute('''
    INSERT OR IGNORE INTO annotation_sources ( annotation_id, source_name)
    VALUES ( :row_id, :source_name )
  ''', {'row_id': row_id, 'source_name': source_name})


def _insert_rule(cursor, record, source_name):
  replacements = {
      'rule_id': record['id'],
      'category': record.get('category'),
      'text': record.get('text'),
      'title': record.get('title'),
      'revision': record.get('revision'),
      'revision_date': record.get('revision_date')
  }

  cursor.execute('''
    INSERT OR REPLACE INTO rules (rule_id, category, canonical_title)
    VALUES (
      :rule_id,
      COALESCE(:category,
               (SELECT category FROM rules WHERE rule_id = :rule_id)),
      COALESCE(:title,
               (SELECT canonical_title FROM rules WHERE rule_id = :rule_id))
    )
  ''', replacements)
  assert(cursor.rowcount > 0)

  if record.get('text') != None:
    logging.debug('About to insert %s', replacements)
    replacements['text_id'] = _get_id(cursor, '''
         -- Matches UNIQUE constraint
         SELECT text_id FROM rule_texts
         WHERE rule_id = :rule_id AND text = :text
         AND (revision = :revision OR (revision IS NULL and :revision IS NULL))
         -- We miss categories from some sources, so try to overwrite NULL
         -- categories
         AND (category = :category OR (category IS NULL OR :category IS NULL))
         LIMIT 1
    ''', replacements)
    if replacements['text_id'] == None:
      logging.info('Inserting rule text for %s/%s', replacements['rule_id'],
          replacements['revision'])
    cursor.execute('''
      INSERT OR REPLACE INTO rule_texts (
        text_id, rule_id, category, title, text, revision, revision_date
      ) VALUES (
        :text_id,
        :rule_id,
        COALESCE(:category,
                 (SELECT category FROM rule_texts WHERE text_id = :text_id)),
        COALESCE(:title,
                 (SELECT title FROM rule_texts WHERE text_id = :text_id)),
        :text,
        :revision,
        COALESCE(:revision_date,
                 (SELECT revision_date FROM rule_texts
                  WHERE text_id = :text_id))
      )
    ''', replacements)
    row_id = cursor.lastrowid

    cursor.execute('''
      INSERT OR IGNORE INTO text_sources (text_id, source_name)
      VALUES (:row_id, :source_name)
    ''', {'row_id': row_id, 'source_name': source_name})

  if 'history' in record:
    for history_entry in record['history']:
      _insert_history(cursor, record['id'], history_entry, source_name)
 
  if 'annotations' in record:
    for annotation_entry in record['annotations']:
      _insert_annotation(cursor, record['id'], annotation_entry,
          record.get('category'),source_name)


def insert_record(cursor, record, source_name):
  if record['type'] == 'rule':
    _insert_rule(cursor, record, source_name)
  elif record['type'] == 'category':
    _insert_category(cursor, record, source_name)
  elif record['type'] == 'annotation':
    _insert_annotation(cursor, None, record, record.get('category'),
        source_name)

def insert_source(cursor, source_name, source_date=None):
  cursor.execute('''
    INSERT OR REPLACE INTO sources (
      source_name, source_date
    ) VALUES (
      :source_name, :source_date
    )
  ''', {
    'source_name': source_name,
    'source_date': _date(source_date)
  })
