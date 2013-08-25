import argparse
import logging
import os
import parse_rule
import subprocess

import rule_db

def _get_revision(revision, rcs_temp_dir, filename):
  subprocess.check_call(
      ['co', '-f' + revision, filename],
      cwd=rcs_temp_dir)
  return open(os.path.join(rcs_temp_dir, filename), 'r')

def _max_revision(rcs_temp_dir, filename):
  with open(os.path.join(rcs_temp_dir, 'RCS', filename + ',v'), 'r') as fh:
    head_line = fh.readline()
    words = head_line.split('\t')
    return int(words[1][2:-2])

def import_flrs(conn, rcs_temp_dir='temp', filename='current_flr.txt'):
  for i in range(1, _max_revision(rcs_temp_dir, filename) + 1):
    with _get_revision('1.' + str(i), rcs_temp_dir, filename) as fh:
      parse_rule.parse_flr(fh,
          lambda record: \
              rule_db.insert_record(conn.cursor(), record,
                filename + '#1.' + str(i))
      )
      conn.commit()

def import_zefram(conn, filename):
  with open(filename, 'r') as fh:
    parse_rule.parse_rule_zefram(fh, 
        lambda record: \
            rule_db.insert_record(conn.cursor(), record, filename)
    )
    conn.commit()

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  conn = rule_db.connect('rules.db')
  import_flrs(conn)
  import_zefram(conn, 'rules_text.txt')

