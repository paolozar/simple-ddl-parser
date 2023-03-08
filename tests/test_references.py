from simple_ddl_parser import DDLParser


def test_references_on():
    expected = [
        {
            "alter": {},
            "checks": [],
            "columns": [
                {
                    "check": None,
                    "default": None,
                    "name": "product_no",
                    "nullable": False,
                    "references": {
                        "column": None,
                        "on_delete": "RESTRICT",
                        "on_update": None,
                        "schema": None,
                        "table": "products",
                        "deferrable_initially": None,
                    },
                    "size": None,
                    "type": "integer",
                    "unique": False,
                },
                {
                    "check": None,
                    "default": None,
                    "name": "order_id",
                    "nullable": False,
                    "references": {
                        "column": None,
                        "on_delete": "CASCADE",
                        "on_update": None,
                        "schema": None,
                        "table": "orders",
                        "deferrable_initially": None,
                    },
                    "size": None,
                    "type": "integer",
                    "unique": False,
                },
                {
                    "check": None,
                    "default": None,
                    "name": "type",
                    "nullable": True,
                    "references": {
                        "column": "type_id",
                        "on_delete": "RESTRICT",
                        "on_update": "CASCADE",
                        "schema": None,
                        "table": "types",
                        "deferrable_initially": None,
                    },
                    "size": None,
                    "type": "integer",
                    "unique": False,
                },
            ],
            "index": [],
            "partitioned_by": [],
            "primary_key": ["product_no", "order_id"],
            "schema": None,
            "table_name": "order_items",
            "tablespace": None,
        }
    ]

    ddl = """
    CREATE TABLE order_items (
        product_no integer REFERENCES products ON DELETE RESTRICT,
        order_id integer REFERENCES orders ON DELETE CASCADE,
        type integer REFERENCES types (type_id) ON UPDATE CASCADE ON DELETE RESTRICT,
        PRIMARY KEY (product_no, order_id)
    );
    """

    result = DDLParser(ddl).run()

    assert expected == result


def test_references():
    ddl = """
    CREATE table users_events(
    event_id  varchar not null REFERENCES events (id),
    user_id varchar not null REFERENCES users (id),
    ) ;
    """
    expected = [
        {
            "columns": [
                {
                    "name": "event_id",
                    "type": "varchar",
                    "size": None,
                    "nullable": False,
                    "default": None,
                    "check": None,
                    "unique": False,
                    "references": {
                        "table": "events",
                        "schema": None,
                        "column": "id",
                        "on_delete": None,
                        "on_update": None,
                        "deferrable_initially": None,
                    },
                },
                {
                    "name": "user_id",
                    "type": "varchar",
                    "size": None,
                    "nullable": False,
                    "default": None,
                    "check": None,
                    "unique": False,
                    "references": {
                        "table": "users",
                        "schema": None,
                        "column": "id",
                        "on_delete": None,
                        "on_update": None,
                        "deferrable_initially": None,
                    },
                },
            ],
            "primary_key": [],
            "index": [],
            "table_name": "users_events",
            "tablespace": None,
            "schema": None,
            "partitioned_by": [],
            "alter": {},
            "checks": [],
        }
    ]
    assert expected == DDLParser(ddl).run()


def test_references_with_schema():
    ddl = """
    create table prod.super_table
    (
        data_sync_id bigint not null default 0,
        id_ref_from_another_table int REFERENCES other_schema.other_table (id),
        primary key (data_sync_id)
    );

    """
    expected = [
        {
            "columns": [
                {
                    "name": "data_sync_id",
                    "type": "bigint",
                    "size": None,
                    "nullable": False,
                    "default": 0,
                    "references": None,
                    "unique": False,
                    "check": None,
                },
                {
                    "name": "id_ref_from_another_table",
                    "type": "int",
                    "size": None,
                    "nullable": True,
                    "default": None,
                    "check": None,
                    "unique": False,
                    "references": {
                        "schema": "other_schema",
                        "column": "id",
                        "table": "other_table",
                        "on_delete": None,
                        "on_update": None,
                        "deferrable_initially": None,
                    },
                },
            ],
            "primary_key": ["data_sync_id"],
            "index": [],
            "table_name": "super_table",
            "tablespace": None,
            "schema": "prod",
            "partitioned_by": [],
            "alter": {},
            "checks": [],
        }
    ]

    parse_results = DDLParser(ddl).run()

    assert expected == parse_results


def test_ref_in_alter():

    ddl = """

    create table ChildTableName(
            parentTable varchar
            );
    ALTER TABLE ChildTableName
    ADD CONSTRAINT "fk_t1_t2_tt"
    FOREIGN KEY ("parentTable")
    REFERENCES parentTable ("columnName")
    ON DELETE CASCADE
    ON UPDATE CASCADE;
    """

    result = DDLParser(ddl).run()
    expected = [
        {
            "alter": {
                "columns": [
                    {
                        "constraint_name": '"fk_t1_t2_tt"',
                        "name": '"parentTable"',
                        "references": {
                            "column": '"columnName"',
                            "on_delete": "CASCADE",
                            "on_update": "CASCADE",
                            "deferrable_initially": None,
                            "schema": None,
                            "table": "parentTable",
                        },
                    }
                ]
            },
            "checks": [],
            "columns": [
                {
                    "check": None,
                    "default": None,
                    "name": "parentTable",
                    "nullable": True,
                    "references": None,
                    "size": None,
                    "type": "varchar",
                    "unique": False,
                }
            ],
            "index": [],
            "partitioned_by": [],
            "primary_key": [],
            "schema": None,
            "table_name": "ChildTableName",
            "tablespace": None,
        }
    ]
    assert expected == result


def test_defferable_initially():
    ddl = """

    CREATE TABLE child (
    id int PRIMARY KEY,
    parent_id int REFERENCES parent
        DEFERRABLE INITIALLY IMMEDIATE,
    name text
    )
    """

    result = DDLParser(ddl).run()
    expected = [
        {
            "alter": {},
            "checks": [],
            "columns": [
                {
                    "check": None,
                    "default": None,
                    "name": "id",
                    "nullable": False,
                    "references": None,
                    "size": None,
                    "type": "int",
                    "unique": False,
                },
                {
                    "check": None,
                    "default": None,
                    "name": "parent_id",
                    "nullable": True,
                    "references": {
                        "column": None,
                        "deferrable_initially": "IMMEDIATE",
                        "on_delete": None,
                        "on_update": None,
                        "schema": None,
                        "table": "parent",
                    },
                    "size": None,
                    "type": "int",
                    "unique": False,
                },
                {
                    "check": None,
                    "default": None,
                    "name": "name",
                    "nullable": True,
                    "references": None,
                    "size": None,
                    "type": "text",
                    "unique": False,
                },
            ],
            "index": [],
            "partitioned_by": [],
            "primary_key": ["id"],
            "schema": None,
            "table_name": "child",
            "tablespace": None,
        }
    ]
    assert expected == result


def test_deferrable_initially_not():

    ddl = """

    CREATE TABLE child (
    id int PRIMARY KEY,
    parent_id int REFERENCES parent
        NOT DEFERRABLE,
    name text
    )
    """

    result = DDLParser(ddl).run()
    expected = [
        {
            "alter": {},
            "checks": [],
            "columns": [
                {
                    "check": None,
                    "default": None,
                    "name": "id",
                    "nullable": False,
                    "references": None,
                    "size": None,
                    "type": "int",
                    "unique": False,
                },
                {
                    "check": None,
                    "default": None,
                    "name": "parent_id",
                    "nullable": True,
                    "references": {
                        "column": None,
                        "deferrable_initially": "NOT",
                        "on_delete": None,
                        "on_update": None,
                        "schema": None,
                        "table": "parent",
                    },
                    "size": None,
                    "type": "int",
                    "unique": False,
                },
                {
                    "check": None,
                    "default": None,
                    "name": "name",
                    "nullable": True,
                    "references": None,
                    "size": None,
                    "type": "text",
                    "unique": False,
                },
            ],
            "index": [],
            "partitioned_by": [],
            "primary_key": ["id"],
            "schema": None,
            "table_name": "child",
            "tablespace": None,
        }
    ]
    assert expected == result


def test_foreigen_keys():
    
    result = DDLParser("""
    CREATE TABLE timeperiod_exceptions (
    exception_id int NOT NULL auto_increment,

    timeperiod_id int NOT NULL,
    days varchar(255) NOT NULL,
    timerange varchar(255) NOT NULL,

    PRIMARY KEY (exception_id),
    INDEX (timeperiod_id),
    FOREIGN KEY (timeperiod_id) REFERENCES timeperiod (tp_id)
        ON DELETE CASCADE
    ) ENGINE=InnoDB CHARACTER SET utf8;
    """, normalize_names=True).run(group_by_type=True)
    expected = {'ddl_properties': [],
    'domains': [],
    'schemas': [],
    'sequences': [],
    'tables': [{'ENGINE=InnoDB': 'CHARACTER',
                'SET': 'utf8',
                'alter': {},
                'checks': [],
                'columns': [{'autoincrement': True,
                            'check': None,
                            'default': None,
                            'name': 'exception_id',
                            'nullable': False,
                            'references': None,
                            'size': None,
                            'type': 'int',
                            'unique': False},
                            {'check': None,
                            'default': None,
                            'name': 'timeperiod_id',
                            'nullable': False,
                            'references': {'column': 'tp_id',
                                            'deferrable_initially': None,
                                            'on_delete': 'CASCADE',
                                            'on_update': None,
                                            'schema': None,
                                            'table': 'timeperiod'},
                            'size': None,
                            'type': 'int',
                            'unique': False},
                            {'check': None,
                            'default': None,
                            'name': 'days',
                            'nullable': False,
                            'references': None,
                            'size': 255,
                            'type': 'varchar',
                            'unique': False},
                            {'check': None,
                            'default': None,
                            'name': 'timerange',
                            'nullable': False,
                            'references': None,
                            'size': 255,
                            'type': 'varchar',
                            'unique': False}],
                'index': [],
                'inline_index': [{'columns': ['timeperiod_id']}],
                'partitioned_by': [],
                'primary_key': ['exception_id'],
                'schema': None,
                'table_name': 'timeperiod_exceptions',
                'tablespace': None}],
    'types': []}
    assert result == expected
