import logging
import sqlite3

def connect(filename):
  cursor = sqlite3.connect(filename)
  cursor.execute('''PRAGMA foreign_keys = ON''')
  return cursor

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

def _insert_history(cursor, rule_id, record, source_name):
  cursor.execute('''
    INSERT OR REPLACE INTO rule_history (
      rule_history_id, rule_id, text, history_date, revision, proposal,
      after_revision
    ) VALUES (
      (SELECT rule_history_id FROM rule_history
       WHERE rule_id = :rule_id AND text = :text
       AND (revision = :revision OR (revision IS NULL AND :revision IS NULL))
       LIMIT 1),
      :rule_id, :text, :date, :revision, :proposal, :after_revision
    )
  ''', {'rule_id': rule_id, 'text': record.get('text'),
        'date': _date(record.get('date')),
        'revision': record.get('revision'),
        'after_revision': record.get('after_revision'),
        'proposal': record.get('proposal')})
  row_id = cursor.lastrowid
  cursor.execute('''
    INSERT OR IGNORE INTO history_sources (
      rule_history_id, source_name
    ) VALUES (:row_id, :source_name)
  ''', {'row_id': row_id, 'source_name': source_name})

def _insert_annotation(cursor, rule_id, record, category, source_name):
  cursor.execute('''
    INSERT OR REPLACE INTO annotations (
      annotation_id, rule_id, text, cfj_ids, cfj_date, category
    ) VALUES (
      -- matches UNIQUE constraint
      (SELECT annotation_id FROM annotations
       WHERE rule_id = :rule_id AND text = :text AND cfj_ids = :cfj_ids
       LIMIT 1),
      :rule_id,
      :text,
      :cfj_ids,
      COALESCE(:cfj_date,
               (SELECT cfj_date FROM rule_annotations WHERE text = :text
                LIMIT 1)),
      COALESCE(:category,
               (SELECT category FROM rule_annotations WHERE text = :text
                LIMIT 1))
    )
  ''', {
    'rule_id': rule_id,
    'text': record['text'],
    'cfj_id': record.get('cfj'),
    'cfj_date': record.get('cfj_date'),
    'category': category,
  })
  row_id = cursor.lastrowid
  cursor.execute('''
    INSERT OR IGNORE INTO annotation_sources ( annotation_id, source_name)
    VALUES ( :row_id, :source_name )
  ''', {'row_id': row_id, 'source_name': source_name})


def _insert_rule(cursor, record, source_name):
  replacements = {
      'rule_id': record['id'],
      'category': record.get('category'),
      'text': record['text'],
      'title': record.get('title'),
      'revision': record.get('revision'),
      'revision_date': record.get('revision_date')
  }

  cursor.execute('''
    INSERT OR REPLACE INTO rules (rule_id, category_name, canonical_title)
    VALUES (
      :rule_id,
      COALESCE(:category_name,
               (SELECT category_name FROM rules WHERE rule_id = :rule_id)),
      COALESCE(:title,
               (SELECT canonical_title FROM rules WHERE rule_id = :rule_id)),
    )
  ''', replacements)
  assert(cursor.rowcount > 0)

  if record['text'] != None:
    logging.info('About to insert %s', replacements)
    # TODO(Charles): Cleaner to select text_id in transaction, then reused
    #                on COALESCEs later.
    cursor.execute('''
      INSERT OR REPLACE INTO rule_texts (
        text_id, rule_id, category, title, text, revision, revision_date
      ) VALUES (
        -- Matches UNIQUE constraint
        (SELECT text_id FROM rule_texts
         WHERE rule_id = :rule_id AND text = :text
         AND (revision = :revision OR (revision IS NULL and :revision IS NULL)
         -- We miss categories from some sources, so try to overwrite NULL
         -- categories
         AND (category = :category OR (category IS NULL OR :category IS NULL)
         LIMIT 1),
        :rule_id,
        COALESCE(:category,
                 (SELECT category FROM rule_texts WHERE rule_id = :rule_id,
                  AND revision = :revision AND revision IS NOT NULL
                  LIMIT 1),
        COALESCE(:title,
                 (SELECT title FROM rule_texts WHERE rule_id = :rule_id
                  AND revision = :revision AND revision IS NOT NULL
                  LIMIT 1)),
        :text,
        :revision,
        COALESCE(:revision_date,
                 (SELECT revision_date FROM rule_texts WHERE rule_id = :rule_id
                  AND revision = :revision AND revision IS NOT NULL
                  LIMIT 1))
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
 
  if 'annotation' in record:
    for annotation_entry in record['annotation']:
      _insert_annotation(cursor, rule['id'], record.get('category'),
                         annotation_entry)


def insert_record(cursor, record, source_name):
  if record['type'] == 'rule':
    _insert_rule(cursor, record, source_name)
  elif record['type'] == 'category':
    _insert_category(cursor, record, source_name)
  elif record['type'] == 'annotation':
    _insert_annotation(cursor, record, source_name)
