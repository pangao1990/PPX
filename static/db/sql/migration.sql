CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 96ee93975f8a

INSERT INTO alembic_version (version_num) VALUES ('96ee93975f8a') RETURNING version_num;

-- Running upgrade 96ee93975f8a -> a69c80be508b

CREATE TABLE ppx_storage_var (
    id INTEGER NOT NULL, 
    "key" VARCHAR NOT NULL, 
    val VARCHAR DEFAULT '' NOT NULL, 
    remark VARCHAR DEFAULT '' NOT NULL, 
    created_at DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), 
    updated_at DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), 
    PRIMARY KEY (id)
);

CREATE INDEX ix_ppx_storage_var_key ON ppx_storage_var ("key");

UPDATE alembic_version SET version_num='a69c80be508b' WHERE alembic_version.version_num = '96ee93975f8a';

-- Running upgrade a69c80be508b -> 802ec4ff5306

DROP INDEX ix_ppx_storage_var_key;

CREATE UNIQUE INDEX ix_ppx_storage_var_key ON ppx_storage_var ("key");

UPDATE alembic_version SET version_num='802ec4ff5306' WHERE alembic_version.version_num = 'a69c80be508b';

