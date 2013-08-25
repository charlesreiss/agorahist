CREATE TABLE rule_categories (
  name STRING NOT NULL PRIMARY KEY,
  description STRING
);

CREATE TABLE rules (
  rule_id INTEGER NOT NULL PRIMARY KEY,

  category_name STRING REFERENCES rule_categories (name),

  canonical_title STRING,
);

CREATE TABLE sources (
  source_name STRING NOT NULL PRIMARY KEY,
  source_date DATE
);

CREATE INDEX sources_by_date ON sources (source_date, source_name);

CREATE TABLE rule_texts (
  text_id INTEGER NOT NULL PRIMARY KEY,
  rule_id INTEGER NOT NULL REFERENCES rules (rule_id),
  text TEXT, -- NULL means repealed
  title TEXT DEFAULT NULL,
  category STRING REFERENCES rule_categories (name),
  revision INTEGER,
  revision_date DATE, -- only for Zefram imports

  -- For manual marking:
  misrecorded BOOLEAN DEFAULT 0,

  UNIQUE (rule_id, text, revision, category)
);

CREATE INDEX rule_texts_by_id_revision ON rule_texts (
  rule_id, revision, revision_date
);

CREATE INDEX rule_texts_by_category ON rule_texts (
  category, rule_id
);

CREATE TABLE text_sources (
  text_id INTEGER NOT NULL REFERENCES rule_texts (text_id),
  source_name STRING NOT NULL REFERENCES sources (source_name),

  UNIQUE (text_id, source_name)
);

CREATE INDEX text_sources_by_text_id ON text_sources (text_id);

CREATE TABLE rule_history (
  rule_history_id INTEGER NOT NULL PRIMARY KEY,
  rule_id INTEGER NOT NULL REFERENCES rules (rule_id),
  text STRING NOT NULL,
  history_date DATE DEFAULT NULL,
  revision INTEGER DEFAULT NULL,
  after_revision INTEGER DEFAULT NULL,
  proposal INTEGER DEFAULT NULL,
  repealed BOOLEAN DEFAULT 0,
  
  -- For manual marking:
  misrecorded BOOLEAN DEFAULT 0,

  old_rule_id INTEGER DEFAULT NULL,
  
  UNIQUE (rule_id, text, revision)
);

CREATE INDEX rule_history_by_id_revision ON rule_history (
  rule_id, revision, after_revision, history_date
);

CREATE TABLE history_sources (
  rule_history_id INTEGER NOT NULL REFERENCES rule_history (rule_history_id),
  source_name STRING NOT NULL REFERENCES sources (source_name),

  UNIQUE (rule_history_id, source_name)
);

CREATE INDEX history_sources_by_history_id ON history_sources (
  rule_history_id
);

-- NB: We currently don't try to store historical rule annotations.
CREATE TABLE annotations (
  annotation_id INTEGER NOT NULL PRIMARY KEY,
  rule_id INTEGER DEFAULT NULL REFERENCES rules (rule_id),
  category STRING DEFAULT NULL REFERENCES rule_categories (name),
  sub_category STRING DEFAULT NULL, -- for non-rule annotations
  -- comma-delimited list of CFJ ids.
  -- note that some annotations have no known CFJ #
  cfj_ids STRING DEFAULT NULL,
  -- date called, if known
  cfj_date DATE,
  text TEXT,

  -- For marking defunct annotations
  historical BOOLEAN DEFAULT 0,

  UNIQUE (rule_id, cfj_ids, text)
);

CREATE INDEX rule_annotation_by_id_category_subcategory ON annotations (
  rule_id, category, sub_category
);

CREATE TABLE annotation_sources (
  annotation_id INTEGER REFERENCES annotations,
  source_name STRING NOT NULL,

  UNIQUE (annotation_id, source_name)
);

CREATE INDEX annotation_sources_by_id ON annotation_sources (annotation_id);
