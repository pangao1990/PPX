CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> f315a762b0fe

CREATE TABLE storage_var (
    id INTEGER NOT NULL, 
    "key" VARCHAR NOT NULL, 
    value VARCHAR DEFAULT '' NOT NULL, 
    created_at DATETIME DEFAULT (CURRENT_TIMESTAMP), 
    updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP), 
    PRIMARY KEY (id)
);

CREATE INDEX ix_storage_var_key ON storage_var ("key");

INSERT INTO alembic_version (version_num) VALUES ('f315a762b0fe') RETURNING version_num;

-- Running upgrade f315a762b0fe -> 86c3f491c4cc

ALTER TABLE storage_var ADD COLUMN remark VARCHAR DEFAULT '' NOT NULL;

UPDATE alembic_version SET version_num='86c3f491c4cc' WHERE alembic_version.version_num = 'f315a762b0fe';

