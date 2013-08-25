import logging
import unittest

import parse_rule

import datetime
import sys
import StringIO

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
),
(
'annotations_after_history',
ur'''Rule 9999/0 (Power=1)     
Some Title
     
      Some text.

History:
Created by Proposal 3558 (General Chaos), Oct. 24 1997

[CFJs 1666-1667 (called 14 May 2007): Where two binding agreements each
construct a partnership, the partnerships have distinct identities even
if the set of partners is the same.]
''',
{
  'id': u'9999',
  'revision': u'0',
  'power': u'1',
  'title': u'Some Title',
  'text': u'Some text.\n',
  'annotations': [
    {'cfj': u'1666,1667',
     'date': datetime.date(2007, 5, 14),
     'text': u'Where two binding agreements each construct a partnership, ' +
             u'the partnerships have distinct identities even if the set ' +
             u'of partners is the same.'
    },
  ],
  'history': [
    {'text': u'Created by Proposal 3558 (General Chaos)',
     'date': datetime.date(1997, 10, 24),
     'proposal': u'3558',
     'revision': u'0',
    },
  ],
},
),
('old_annotations',
ur'''Rule 101/1 (Power=3)
Obey the Rules                                                                  
                                                                                
      Some text.

CFJ 1103 (Judged TRUE, Aug. 21 1998): "In the case of conflict
 between Rules of unequal Power, ..."

[CFJ ???: "abide by all the Rules" means the Rules as a whole, not              
 necessarily each individual Rule.                                              
 CFJ 24: Players must obey the Rules even in out-of-game actions.               
 CFJ 825: Players would have to obey the Rules even if 101 were                 
 repealed.                                                                      
 CFJ 1132, Judged May 18, 1999: A Player failing to perform a duty              
 required by the Rules within a reasonable time may be in violation             
 of the Rules, even if the Rules do not provide a time limit for                
 the performance of that duty.
 CFJs 815 & 816: If an amendment is made which changes the properties           
 of an Entity, STUFF. 
 CFJ 1112, Judged TRUE Jan. 21 1999: "In order to submit a Proposal,            
 in the sense of R1865 and elsewhere, STUFF."
 CFJ 1110 (Judged Dec. 11 1998; Appeal completed Dec. 22 1998) &
 CFJ 1111 (Judged Dec. 22 1998): When the voting period of a proposal
 whose voting period is in progress...]

[CFJ 1139: Interpretations [judgements at the time of CFJ 1139] need
not necessairily accord with the reasoning and arguments of Judges or
Justices given in past CFJs.]

History:                                                                        
Initial Immutable Rule 101, Jun. 30 1993                                        
Mutated from MI=Unanimity to MI=3 by Proposal 1480, Mar. 15 1995                
''',
{'id': u'101',
 'revision': u'1',
 'title': u'Obey the Rules',
 'text': u'Some text.\n',
 'power': u'3',
 'history': [
   {'text': u'Initial Immutable Rule 101',
    'date': datetime.date(1993, 6, 30),
    'revision': u'0',
   },
   {'text': u'Mutated from MI=Unanimity to MI=3 by Proposal 1480',
    'date': datetime.date(1995, 3, 15),
    'after_revision': u'0',
    'proposal': u'1480',
   },
  ],
 # Expect these sorted by cfj ID
 'annotations': [
   {'text': u'"abide by all the Rules" means the Rules as a whole, not ' +
            u'necessarily each individual Rule.'},
   {'cfj': u'24',
    'text': u'Players must obey the Rules even in out-of-game actions.',
    },
   {'cfj': u'815,816',
    'text': u'If an amendment is made which changes the properties of an ' +
    'Entity, STUFF.',
    },
   {'cfj': u'825',
    'text': u'Players would have to obey the Rules even if 101 were ' +
            u'repealed.',
    },
   {'cfj': u'1103',
    'judged_date': datetime.date(1998, 8, 21),
    'text': u'In the case of conflict between Rules of unequal Power, ...',
    },
   {'cfj': u'1110,1111',
    'judged_date': datetime.date(1998, 12, 22),
    'text': u'When the voting period of a proposal whose voting period is ' +
            u'in progress...'
    },
   {'cfj': u'1112',
    'judged_date': datetime.date(1999, 1, 21),
    'text': u'In order to submit a Proposal, in the sense of R1865 and ' +
            u'elsewhere, STUFF.'
    },
   {'cfj': u'1132',
    'judged_date': datetime.date(1999, 5, 18),
    'text': u'A Player failing to perform a duty required by the Rules ' +
    'within a reasonable time may be in violation of the Rules, even if the ' +
    'Rules do not provide a time limit for the performance of that duty.'},
   {'cfj': u'1139',
    'text': u'Interpretations [judgements at the time of CFJ 1139] need not ' +
            u'necessairily accord with the reasoning and arguments of Judges ' +
            u'or Justices given in past CFJs.'},
  ]
}),
('multiline_hist',
ur'''Rule 42/0 (Power=1)
Some Title

      Some text.

History:
Created by Proposal 9999 (foo, bar, baz, quux,
  beta, omega), 30 July 2010
Amended(12) by Proposal 3990, "Harsher Blot Penalties", (Elysion),              
  Mar. 30 2000 
''',
{'id': u'42',
 'revision': u'0',
 'power': u'1',
 'title': u'Some Title',
 'text': u'Some text.\n',
 'history': [
    {'text': u'Created by Proposal 9999 (foo, bar, baz, quux, beta, omega)',
     'date': datetime.date(2010, 7, 30),
     'proposal': u'9999',
     'revision': u'0'},
    {'text': u'Amended(12) by Proposal 3990, "Harsher Blot Penalties", ' +
             u'(Elysion)',
     'date': datetime.date(2000, 3, 30),
     'proposal': u'3990',
     'revision': u'12'},
  ],
 }),
('repealed_notext',
ur'''Rule 42/1 (Power=1)
Some Title


History:
Created by Proposal 9999 (foo), 29 July 2010
Repealed by Proposal 8888 (bar), 30 July 2010
''',
{'id': u'42',
 'power': u'1',
 'revision': u'1',
 'title': u'Some Title',
 'text': u'',
 'repealed': True,
 'history': [
   {'text': u'Created by Proposal 9999 (foo)',
    'date': datetime.date(2010, 7, 29),
    'proposal': u'9999',
    'revision': u'0'},
   {'text': u'Repealed by Proposal 8888 (bar)',
    'date': datetime.date(2010, 7, 30),
    'proposal': u'8888',
    'repeal': True,
    'after_revision': u'0'},
 ],
}),
('repealed_sometext',
ur'''Rule 42/1 (Power=1)
Some Title

    Some text.

History:
Created by Proposal 9999 (foo), 29 July 2010
Repealed by Proposal 8888 (bar), 30 July 2010
''',
{'id': u'42',
 'power': u'1',
 'revision': u'1',
 'title': u'Some Title',
 'text': u'Some text.\n',
 'repealed': True,
 'history': [
   {'text': u'Created by Proposal 9999 (foo)',
    'date': datetime.date(2010, 7, 29),
    'proposal': u'9999',
    'revision': u'0'},
   {'text': u'Repealed by Proposal 8888 (bar)',
    'date': datetime.date(2010, 7, 30),
    'proposal': u'8888',
    'after_revision': u'0',
    'repeal': True},
 ],
}),
]

HISTORY_CASES = [
  ('repealed',
   u'Repealed by Proposal 1234 (Foo), 24 August 2013',
   {'text': u'Repealed by Proposal 1234 (Foo)',
    'date': datetime.date(2013, 8, 24),
    'proposal': u'1234',
    'repeal': True
    }),
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
  ('amended_substantial2',
   u'Amended(1) by Proposal 2795 (Andre), Jan. 30 1997, substantial ' +
   u'(unattributed)',
   {'text': u'Amended(1) by Proposal 2795 (Andre), substantial (unattributed)',
    'date': datetime.date(1997, 1, 30),
    'proposal': u'2795',
    'revision': u'1',
    },
  ),
  ('amended_substantial_misspelled',
   u'Amended(1) by Proposal 2795 (Andre), Jan. 30 1997, susbtantial ' +
   u'(unattributed)',
   {'text': u'Amended(1) by Proposal 2795 (Andre), susbtantial (unattributed)',
    'date': datetime.date(1997, 1, 30),
    'proposal': u'2795',
    'revision': u'1',
    },
  ),
  ('amended_cosmetic',
   u'Amended(7) by Proposal 2830 (Murphy), Mar. 7 1997, cosmetic\n' + 
   u'  (unattributed)',
   {'text': u'Amended(7) by Proposal 2830 (Murphy), cosmetic (unattributed)',
    'date': datetime.date(1997, 3, 7),
    'proposal': u'2830',
    'revision': u'7',
    }),
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
  ('created_funnynum',
   u'Created by Proposal 01-005 (Steve), Feb. 2 2001',
   {'text': u'Created by Proposal 01-005 (Steve)',
    'date': datetime.date(2001, 2, 2),
    'revision': u'0',
    'proposal': u'01-005',
    }),
  ('amended_funnynum',
   u'Amended(6) by Proposal 535[2001] (Elysion), Feb. 2 2001',
   {'text': u'Amended(6) by Proposal 535[2001] (Elysion)',
    'date': datetime.date(2001, 2, 2),
    'revision': u'6',
    'proposal': u'535[2001]',
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

FLR_CASES = [
    ('one_rule_one_orphan_cfj',
ur"""THE FULL LOGICAL RULESET

----------------------------------------------------------------------

Not a rule.

----------------------------------------------------------------------

======================================================================
Table of Contents

  Some stuff.
----------------------------------------------------------------------

======================================================================
The Game of Agora
      A category concerning this nomic generally, constitutional
      matters, and relationships between the most fundamental nomic
      entities.
----------------------------------------------------------------------

Rule 101/0 (Power=3)
The Rights of Agorans

  Sample text.

History:
Initial rule 101, 1 Jan 2010

----------------------------------------------------------------------

======================================================================
Catch-All Category
      A miscellaneous category.
----------------------------------------------------------------------

Sub-category name

[CFJ 1892 (called 2 February 2008): An agreement that is not binding
is thereby not a contract.]

----------------------------------------------------------------------

""",
[{'type': 'category',
  'name': u'The Game of Agora',
  'description': u'A category concerning this nomic generally, constitutional ' +
  u'matters, and relationships between the most fundamental nomic entities.'
  },
 {'type': 'rule',
  'title': u'The Rights of Agorans',
  'id': u'101', 'revision': u'0', 
  'text': u'Sample text.\n',
  'history': [{'text': u'Initial rule 101', 'date': datetime.date(2010, 1, 1),
               'revision': u'0'}],
  'power': u'3',
  'category': u'The Game of Agora',
  },
 {'type': 'category',
   'name': u'Catch-All Category',
   'description': u'A miscellaneous category.',
  },
 {'type': 'annotation',
  'category': u'Catch-All Category',
  'subcategory': u'Sub-category name',
  'cfj': u'1892',
  'date': datetime.date(2008, 2, 2),
  'text': u'An agreement that is not binding is thereby not a contract.'}])
]

class ParseRuleFLRTest(unittest.TestCase):
  def _test_one(self, input, output):
    self.maxDiff = None
    parsed = parse_rule.parse_rule_flr(input)
    if parsed != None and output != None and \
       'text' in parsed and 'text' in output:
      # Test text separately for better errors.
      self.assertEqual(output['text'], parsed['text'])
    self.assertDictEqual(output, parsed)

class ParseRuleZeframTest(unittest.TestCase):
  def _test_one(self, input, output):
    self.maxDiff = None
    parsed = parse_rule.parse_rule_zefram(input)
    self.assertEqual(len(parsed), len(output))
    for parsed_item, output_item in zip(parsed, output):
      self.assertDictEqual(output_item, parsed_item)

class ParseHistoryTest(unittest.TestCase):
  def _test_one(self, input, output):
    self.assertDictEqual(output, parse_rule._parse_history_line(input))

class ParseFLRTest(unittest.TestCase):
  def _test_one(self, input, output):
    current_parse = []
    parse_rule.parse_flr(StringIO.StringIO(input), lambda d: current_parse.append(d))
    self.assertListEqual(output, current_parse)

def _make_test(o, label, input, output):
  setattr(o, 'test_' + label,
      lambda self: self._test_one(input, output))

def _generate_tests():
  for label, input, output in RULE_CASES:
    _make_test(ParseRuleFLRTest, label, input, output)
  for label, input, output in HISTORY_CASES:
    _make_test(ParseHistoryTest, label, input, output)
  for label, input, output in FLR_CASES:
    _make_test(ParseFLRTest, label, input, output)

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
  _generate_tests()
  unittest.main()
