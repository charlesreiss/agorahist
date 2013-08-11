import logging
import unittest

import parse_rule

import datetime
import sys

RULE_CASES = [
("flr_map",
ur"""Rule 2105/5 (Power=1)
The Map of Agora

                               ____  _        /|
                    DARWIN ->  \_  |/ |      / \
                              __/    /      |  |
            <- DSV          /      /        |  \
                        _   \      \_       |   \
                  MORNINGTON CRESCENT ->    /    |  <- GOETHE BARRIER
                 _ _/       |         \_/\_/     \     REEF
                / \\ <- SHARK BAY      |         |
               /            |          |          \ <- TOWNSVILLE
            ___/            |          |           \_
         __/                |          |  .___o  )   |
        /                   |          | ~~vv ===~~~ <-OSCAR'S MIRE
       /           O <- SHERLOCK NESS  |             |/\
      |                     |          |               |_
      |                     |          |  EMERALD ->     \
      \                     |__________=_____,             \ BRISBANE
       /                    |                |             | <-'
       \      O <- LT. ANNE MOORE            |        __  _\
        \                   |                |_______/  \/ |  LORD
         |                __/\      <- TARACOOLA          /   HOWE ->
         \  PERTH      __/    \_             /           /
          | <-'  _  __/         |   /| IVANHOE ->       | <-.
          /    _/ \/             \ / /       |         /  WOLLONGONG
         |_   /     <- ESPERANTO  v /__     |_        / <- CANBERRA
           \_/                         \    | \_    _|
                  __   __              |    |   \__/           \_
                 __ \ / __              \___=_  ___|            \_
                /  \ | /  \     MANUBOURNE -> \/      NEW C.LAND \}
                    \|/                                           \)
               _,.---v---._                 /\__                   )`-']
      /\__/\  /            \                |   |  COOK SCSTRAIGHT(    !
      \_  _/ /              \                |  /      MICHAELTON->)  /
        \ \_|           @ __|                \_/ <- HOBART    |^\  (_/
         \                \_                                 (  |
          \     ,__/       /                                 /  *
        ~~~`~~~~~~~~~~~~~~/~~~~                  BREE_523->/~   /
                                            MURPHENDELL--> #   /
                                                         /   |BOBCHURCH
                                             PAVRITTON->/  _|
                                                       {__/
                                                     /  @
                                    WOOBLEING HEIGHTS

History:
Created by Proposal 4735 (Maud), 5 May 2005
Amended(1) by Proposal 4807 (Sherlock), 15 June 2005
Amended(2) by Proposal 4866 (Goethe), 27 August 2006
Amended(3) by Proposal 4946 (Zefram), 3 May 2007
Amended(4) by Proposal 6581 (G.), 28 November 2009
Amended(5) by Proposal 7210 (scshunt), 4 May 2012""",
{
    'id': u'2105',
    'revision': u'5',
    'power': u'1',
    'title': u'The Map of Agora',
    'text':
ur"""                         ____  _        /|
              DARWIN ->  \_  |/ |      / \
                        __/    /      |  |
      <- DSV          /      /        |  \
                  _   \      \_       |   \
            MORNINGTON CRESCENT ->    /    |  <- GOETHE BARRIER
           _ _/       |         \_/\_/     \     REEF
          / \\ <- SHARK BAY      |         |
         /            |          |          \ <- TOWNSVILLE
      ___/            |          |           \_
   __/                |          |  .___o  )   |
  /                   |          | ~~vv ===~~~ <-OSCAR'S MIRE
 /           O <- SHERLOCK NESS  |             |/\
|                     |          |               |_
|                     |          |  EMERALD ->     \
\                     |__________=_____,             \ BRISBANE
 /                    |                |             | <-'
 \      O <- LT. ANNE MOORE            |        __  _\
  \                   |                |_______/  \/ |  LORD
   |                __/\      <- TARACOOLA          /   HOWE ->
   \  PERTH      __/    \_             /           /
    | <-'  _  __/         |   /| IVANHOE ->       | <-.
    /    _/ \/             \ / /       |         /  WOLLONGONG
   |_   /     <- ESPERANTO  v /__     |_        / <- CANBERRA
     \_/                         \    | \_    _|
            __   __              |    |   \__/           \_
           __ \ / __              \___=_  ___|            \_
          /  \ | /  \     MANUBOURNE -> \/      NEW C.LAND \}
              \|/                                           \)
         _,.---v---._                 /\__                   )`-']
/\__/\  /            \                |   |  COOK SCSTRAIGHT(    !
\_  _/ /              \                |  /      MICHAELTON->)  /
  \ \_|           @ __|                \_/ <- HOBART    |^\  (_/
   \                \_                                 (  |
    \     ,__/       /                                 /  *
  ~~~`~~~~~~~~~~~~~~/~~~~                  BREE_523->/~   /
                                      MURPHENDELL--> #   /
                                                   /   |BOBCHURCH
                                       PAVRITTON->/  _|
                                                 {__/
                                               /  @
                              WOOBLEING HEIGHTS
""",
    'history': [
      {'text': u'Created by Proposal 4735 (Maud)',
       'date': datetime.date(2005, 5, 5),
       'proposal': u'4735',
       'revision': u'0'},
      {'text': u'Amended(1) by Proposal 4807 (Sherlock)',
       'date': datetime.date(2005, 6, 15),
       'proposal': u'4807',
       'revision': u'1'},
      {'text': u'Amended(2) by Proposal 4866 (Goethe)',
       'date': datetime.date(2006, 8, 27),
       'proposal': u'4866',
       'revision': u'2'},
      {'text': u'Amended(3) by Proposal 4946 (Zefram)',
       'date': datetime.date(2007, 5, 3),
       'proposal': u'4946',
       'revision': u'3'},
      {'text': u'Amended(4) by Proposal 6581 (G.)',
       'date': datetime.date(2009, 11, 28),
       'proposal': u'6581',
       'revision': u'4'},
      {'text': u'Amended(5) by Proposal 7210 (scshunt)',
       'date': datetime.date(2012, 5, 4),
       'proposal': u'7210',
       'revision': u'5'},
    ],
}),
(
'flr_1586_8_trunc_hist',
ur'''Rule 1586/8 (Power=2)
Definition and Continuity of Entities

      If multiple rules attempt to define an entity with the same
      name, then they refer to the same entity.  A rule-defined
      entity's name CANNOT be changed to be the same as another
      rule-defined entity's name.

      A rule referring to an entity by name refers to the entity that
      had that name when the rule first came to include that
      reference, even if the entity's name has since changed.

      If the rules are amended such that they no longer define an
      entity, then that entity and its attributes cease to exist.

      If the rules are amended such that they define an entity both
      before and after the amendment, but with different attributes,
      then that entity and its attributes continue to exist to
      whatever extent is possible under the new definitions.

[CFJ 1807 (called 25 November 2007): Rule-defined entities include
pending timed events, which can therefore occur under modified rules
even if the events that originally triggered them would not trigger
them under the new rules.]

[CFJ 1922 (called 4 April 2008): Without legislation to the contrary,
documents attempting to define an entity with the same name define
distinct entities.]

History:
Created by Proposal 2481, Feb. 16 1996
Amended(1) by Proposal 2795 (Andre), Jan. 30 1997, substantial''',
{
  'id': u'1586',
  'revision': u'8',
  'power': u'2',
  'title': u'Definition and Continuity of Entities',
  'text': ur'''If multiple rules attempt to define an entity with the same
name, then they refer to the same entity.  A rule-defined
entity's name CANNOT be changed to be the same as another
rule-defined entity's name.

A rule referring to an entity by name refers to the entity that
had that name when the rule first came to include that
reference, even if the entity's name has since changed.

If the rules are amended such that they no longer define an
entity, then that entity and its attributes cease to exist.

If the rules are amended such that they define an entity both
before and after the amendment, but with different attributes,
then that entity and its attributes continue to exist to
whatever extent is possible under the new definitions.
''',
    'annotations': [
      {'cfj': u'1807',
       'date': datetime.date(2007, 11, 25),
       'text': u'Rule-defined entities include pending timed events, which ' +
       u'can therefore occur under modified rules even if the events that ' +
       u'originally triggered them would not trigger them under the new rules.',
      },
      {'cfj': u'1922',
       'date': datetime.date(2008, 4, 4),
       'text': u'Without legislation to the contrary, documents attempting ' +
       u'to define an entity with the same name define distinct entities.'},
    ],
    'history': [
      {'text': u'Created by Proposal 2481',
       'date': datetime.date(1996, 2, 16),
       'proposal': u'2481',
       'revision': u'0',
       },
      {'text': u'Amended(1) by Proposal 2795 (Andre), substantial',
       'date': datetime.date(1997, 1, 30),
       'proposal': u'2795',
       'revision': u'1',
       },
    ]
},
)
]

HISTORY_CASES = [
  ('created',
   u'Created by Proposal 4735 (Maud), 5 May 2005',
   {'text': u'Created by Proposal 4735 (Maud)',
    'date': datetime.date(2005, 5, 5),
    'proposal': u'4735',
    'revision': u'0'}),
  ('amended1',
    u'Amended(1) by Proposal 4807 (Sherlock), 15 June 2005',
      {'text': u'Amended(1) by Proposal 4807 (Sherlock)',
       'date': datetime.date(2005, 6, 15),
       'proposal': u'4807',
       'revision': u'1'}),
  ('created_alt_date',
   u'Created by Proposal 2481, Feb. 16 1996',
   {'text': u'Created by Proposal 2481',
    'date': datetime.date(1996, 2, 16),
    'proposal': u'2481',
    'revision': u'0',
    },
  ),
  ('amended_substantial',
   u'Amended(1) by Proposal 2795 (Andre), Jan. 30 1997, substantial',
   {'text': u'Amended(1) by Proposal 2795 (Andre), substantial',
    'date': datetime.date(1997, 1, 30),
    'proposal': u'2795',
    'revision': u'1',
    },
  ),
  ('power_changed',
   u'Power changed from 1 to 2 by Proposal 3999 (harvel), May 2 2000',
   {'text': u'Power changed from 1 to 2 by Proposal 3999 (harvel)',
    'date': datetime.date(2000, 5, 2),
    'proposal': u'3999',
    },
  ),
  ('cleaning',
    u'Amended(6) by cleaning (comex), 26 January 2009',
    {'text': u'Amended(6) by cleaning (comex)',
     'date': datetime.date(2009, 1, 26),
     'revision': u'6',
    },
  ),
  ('mutated',
   u'Mutated from M=Unanimity to MI=3 by Proposal 1480, 15 March 1995',
   {'text': u'Mutated from M=Unanimity to MI=3 by Proposal 1480',
    'date': datetime.date(1995, 3, 15),
    'proposal': u'1480',
   },
  ),
  ('retitled',
   u'Retitled by Proposal 4944 (Zefram), 3 May 2007',
   {'text': u'Retitled by Proposal 4944 (Zefram)',
    'date': datetime.date(2007, 5, 3),
    'proposal': u'4944',
    }
  ),
  ('renumbered',
   u'Renumbered from 1072 to 105 by Rule 1295, 1 November 1994',
   {'text': u'Renumbered from 1072 to 105 by Rule 1295',
    'date': datetime.date(1994, 11, 1),
   }
  ),
  ('infected',
   u'Infected and Amended(4) by Rule 1454, 27 July 1996',
   {'text': u'Infected and Amended(4) by Rule 1454',
    'date': datetime.date(1996, 7, 27),
    'revision': u'4',
    }
  ),
  ('amended_nonum',
   u'Amended(8) by Proposal "A Separation of Powers" (Steve, ' +
   u'Without Objection), 20 April 1999',
   {'text': u'Amended(8) by Proposal "A Separation of Powers" (Steve, ' +
            u'Without Objection)',
    'date': datetime.date(1999, 4, 20),
    'revision': u'8',
    'proposal': u'A Separation of Powers',
   }),
  ('initial',
   u'Initial Immutable Rule 101, 30 June 1993',
   {'text': 'Initial Immutable Rule 101',
    'date': datetime.date(1993, 6, 30),
    'revision': u'0',
   }),
]

ZEFRAM_CASES = [
('multiple_versions',
ur'''

RULE 101

history: Initial Immutable Rule 101, 30 June 1993

[Have 2 texts for this nominal revision, differing trivially.]

text:

      Shortened sample text.

text:

      Shortened sample text.
      With multiple lines.

history: Mutated from MI=Unanimity to MI=3 by Proposal 1480, 15 March 1995

history: Amended(1) by Proposal 3915 (harvel), 27 September 1999

text:

      Revision 1 sample text. 

history: ...
''',
[{'id': u'101',
  'history': [
    {'text': 'Initial Immutable Rule 101',
     'date': datetime.date(1993, 6, 30),
     'revision': u'0',
     },
    {'text': 'Mutated from MI=Unanimity to MI=3 by Proposal 1480',
     'date': datetime.date(1995, 3, 15),
     'proposal': u'1480',
     },
    {'text': 'Amended(1) by Proposal 3915 (harvel)',
     'date': datetime.date(1999, 9, 27),
     'proposal': u'3915',
     'revision': u'1'},
   ],
 },
 {'id': u'101',
  'text': u'Shortened sample text.\n',
  'revision': u'0',
  'date': datetime.date(1993, 6, 30),
 },
 {'id': u'101',
  'text': u'Shortened sample text.\nWith multiple lines.\n',
  'revision': u'0',
  'date': datetime.date(1993, 6, 30),
 },
 {'id': u'101',
  'text': u'Revision 1 sample text.\n',
  'revision': u'1',
  'date': datetime.date(1999, 9, 27),
 },
]),
]

class ParseRuleFLRTest(unittest.TestCase):
  def _test_one(self, input, output):
    self.maxDiff = None
    parsed = parse_rule.parse_rule_flr(input)
    if 'text' in parsed and 'text' in output:
      # Test text separately for better errors.
      self.assertEqual(output['text'], parsed['text'])
    self.assertDictEqual(output, parse_rule.parse_rule_flr(input))
  pass

class ParseRuleZeframTest(unittest.TestCase):
  def _test_one(self, input, output):
    self.maxDiff = None
    parsed = parse_rule.parse_rule_zefram(input)
    self.assertEqual(len(parsed), len(output))
    for parsed_item, output_item in zip(parsed, output):
      self.assertDictEqual(output_item, parsed_item)
  pass

class ParseHistoryTest(unittest.TestCase):
  def _test_one(self, input, output):
    self.assertDictEqual(output, parse_rule._parse_history_line(input))
  pass

def _make_test(o, label, input, output):
  setattr(o, 'test_' + label,
      lambda self: self._test_one(input, output))


def _generate_tests():
  for label, input, output in RULE_CASES:
    _make_test(ParseRuleFLRTest, label, input, output)
  for label, input, output in HISTORY_CASES:
    _make_test(ParseHistoryTest, label, input, output)

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
  _generate_tests()
  unittest.main()
