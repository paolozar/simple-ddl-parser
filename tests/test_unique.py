from simple_ddl_parser import DDLParser


def test_unique_statements():
    result = DDLParser("""
    CREATE TABLE testtbl1 (
            fld1 int UNIQUE,
            fld2 int UNIQUE
    );

    CREATE TABLE testtbl2 (
            fld1 int,
            fld2 int,
            UNIQUE (fld1, fld2)
    );

    CREATE TABLE testtbl3 (
            fld1 int,
            fld2 int,
            UNIQUE (fld1),
            UNIQUE (fld2)
    );

    CREATE TABLE testtbl4 (
            fld1 int,
            fld2 int,
            UNIQUE (fld1),
            CONSTRAINT testtbl4_idx UNIQUE (fld2)
    );

    CREATE TABLE testtbl5 (
            fld1 int,
            fld2 int,
    );
    ALTER TABLE ONLY testtbl5 ADD CONSTRAINT fld1_key UNIQUE (fld1);
    ALTER TABLE ONLY testtbl5 ADD CONSTRAINT fld2_key UNIQUE (fld2);

    CREATE TABLE testtbl6 (
            fld1 int,
            fld2 int,
    );
    ALTER TABLE ONLY testtbl6 ADD CONSTRAINT fld1_fld2_key UNIQUE (fld1, fld2);
    """
    ).run()

    expected = [
        {
            'table_name': 'testtbl1',
            'schema': None,
            'partitioned_by': [],
            'tablespace': None,
            'columns': [
                {
                    'name': 'fld1',
                    'type': 'int',
                    'size': None,
                    'references': None,
                    'unique': True,
                    'nullable': True,
                    'default': None,
                    'check': None
                },
                {'name': 'fld2',
                 'type': 'int',
                 'size': None,
                 'references': None,
                 'unique': True,
                'nullable': True,
                 'default': None,
                 'check': None
             }
            ],
            'primary_key': [],
            'alter': {},
            'checks': [],
            'index': []
        },
        {
            'table_name': 'testtbl2',
            'schema': None,
            'partitioned_by': [],
            'tablespace': None,
            'columns': [
                {
                    'name': 'fld1',
                    'type': 'int',
                    'size': None,
                    'references': None,
                    'unique': False,
                    'nullable': True,
                    'default': None,
                    'check': None
                },
                {
                    'name': 'fld2',
                    'type': 'int',
                    'size': None,
                    'references': None,
                    'unique': False,
                    'nullable': True,
                    'default': None,
                    'check': None
                }
            ],
            'primary_key': [],
            'alter': {},
            'checks': [],
            'index': [],
            'uniques': [
                {'columns': ['fld1', 'fld2']}
            ]
        },
        {
            'table_name': 'testtbl3',
            'schema': None,
            'partitioned_by': [],
            'tablespace': None,
            'columns': [
                {
                    'name': 'fld1',
                    'type': 'int',
                    'size': None,
                    'references': None,
                    'unique': False,
                    'nullable': True,
                    'default': None,
                    'check': None
                },
                {
                    'name': 'fld2',
                    'type': 'int',
                    'size': None,
                    'references': None,
                    'unique': False,
                    'nullable': True,
                    'default': None,
                    'check': None
                }
            ],
            'primary_key': [],
            'alter': {},
            'checks': [],
            'index': [],
            'uniques': [
                {'columns': ['fld1']},
                {'columns': ['fld2']}
            ]
        },
        {
            'table_name': 'testtbl4',
            'schema': None,
            'partitioned_by': [],
            'tablespace': None,
            'columns': [
                {
                    'name': 'fld1',
                    'type': 'int',
                    'size': None,
                    'references': None,
                    'unique': False,
                    'nullable': True,
                    'default': None,
                    'check': None
                },
                {
                    'name': 'fld2',
                    'type': 'int',
                    'size': None,
                    'references': None,
                'unique': False,
                    'nullable': True,
                    'default': None,
                    'check': None}],
            'primary_key': [],
            'alter': {},
            'checks': [],
            'index': [],
            'uniques': [
                {'columns': ['fld1']}
            ],
            'constraints': {
                'uniques': [
                    {
                        'columns': ['fld2'],
                        'constraint_name': 'testtbl4_idx'
                    }
                ]
            }
        },
        {
            'table_name': 'testtbl5',
            'schema': None,
            'partitioned_by': [],
            'tablespace': None,
            'columns': [
                {
                    'name': 'fld1',
                    'type': 'int',
                    'size': None,
                    'references': None,
                    'unique': False,
                    'nullable': True,
                    'default': None,
                    'check': None
                },
                {
                    'name': 'fld2',
                    'type': 'int',
                    'size': None,
                    'references': None,
                    'unique': False,
                    'nullable': True,
                    'default': None,
                    'check': None
                }
            ],
            'primary_key': [],
            'alter': {
                'uniques': [
                    {
                        'constraint_name': 'fld1_key',
                        'columns': ['fld1']
                    },
                    {
                        'constraint_name': 'fld2_key',
                        'columns': ['fld2']
                    }
                ]
            },
            'checks': [],
            'index': []
        },
        {
            'table_name': 'testtbl6',
            'schema': None,
            'partitioned_by': [],
            'tablespace': None,
            'columns': [
                {
                    'name': 'fld1',
                    'type': 'int',
                    'size': None,
                    'references': None,
                    'unique': False,
                    'nullable': True,
                    'default': None,
                    'check': None
                },
                {
                    'name': 'fld2',
                    'type': 'int',
                    'size': None,
                    'references': None,
                    'unique': False,
                    'nullable': True,
                    'default': None,
                    'check': None
                }
            ],
            'primary_key': [],
            'alter': {
                'uniques': [
                    {
                        'constraint_name': 'fld1_fld2_key',
                        'columns': ['fld1', 'fld2']
                    }
                ]
            },
            'checks': [],
            'index': []}
    ]
    assert result == expected
