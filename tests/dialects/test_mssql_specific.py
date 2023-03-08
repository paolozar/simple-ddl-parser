from simple_ddl_parser import DDLParser


def test_int_identity_type():
    ddl = """
    CREATE TABLE sqlserverlist (

    id INT IDENTITY (1,1) PRIMARY KEY, -- NOTE
    company_id BIGINT ,
    )
    """

    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        "comments": [" NOTE"],
        "ddl_properties": [],
        "sequences": [],
        "domains": [],
        "schemas": [],
        "tables": [
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
                        "size": (1, 1),
                        "type": "INT IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "company_id",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "BIGINT",
                        "unique": False,
                    },
                ],
                "index": [],
                "partitioned_by": [],
                "primary_key": ["id"],
                "schema": None,
                "table_name": "sqlserverlist",
                "tablespace": None,
            }
        ],
        "types": [],
    }
    assert expected == result


def test_mssql_foreign_ref_in_column():

    ddl = """
    CREATE TABLE sqlserverlist (

    id INT IDENTITY (1,1) PRIMARY KEY, -- NOTE
    company_id BIGINT ,
    primary_id INT FOREIGN KEY REFERENCES Persons(PersonID), -- ADD THIS COLUMN FOR THE FOREIGN KEY
    )
    """

    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        'comments': [' NOTE', ' ADD THIS COLUMN FOR THE FOREIGN KEY'],
        "ddl_properties": [],
        "sequences": [],
        "domains": [],
        "schemas": [],
        "tables": [
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
                        "size": (1, 1),
                        "type": "INT IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "company_id",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "BIGINT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "primary_id",
                        "nullable": True,
                        "references": {
                            "column": "PersonID",
                            "deferrable_initially": None,
                            "on_delete": None,
                            "on_update": None,
                            "schema": None,
                            "table": "Persons",
                        },
                        "size": None,
                        "type": "INT",
                        "unique": False,
                    },
                ],
                "index": [],
                "partitioned_by": [],
                "primary_key": ["id"],
                "schema": None,
                "table_name": "sqlserverlist",
                "tablespace": None,
            }
        ],
        "types": [],
    }
    assert expected == result


def test_max_supported_as_column_size():
    ddl = """
    CREATE TABLE sqlserverlist (

    user_account VARCHAR(8000) NOT NULL,
    user_first_name VARCHAR(max) NOT NULL,
    )
    """
    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        "sequences": [],
        "ddl_properties": [],
        "domains": [],
        "schemas": [],
        "tables": [
            {
                "alter": {},
                "checks": [],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "user_account",
                        "nullable": False,
                        "references": None,
                        "size": 8000,
                        "type": "VARCHAR",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_first_name",
                        "nullable": False,
                        "references": None,
                        "size": "max",
                        "type": "VARCHAR",
                        "unique": False,
                    },
                ],
                "index": [],
                "partitioned_by": [],
                "primary_key": [],
                "schema": None,
                "table_name": "sqlserverlist",
                "tablespace": None,
            }
        ],
        "types": [],
    }
    assert expected == result


def test_constraint_unique():
    ddl = """
    CREATE TABLE sqlserverlist (

    id INT IDENTITY (1,1) PRIMARY KEY, -- NOTE
    company_id BIGINT ,
    user_last_name 	VARBINARY(8000) NOT NULL,
    CONSTRAINT UC_sqlserverlist_last_name UNIQUE (company_id,user_last_name)
    )
    """

    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        "comments": [" NOTE"],
        "sequences": [],
        "ddl_properties": [],
        "domains": [],
        "schemas": [],
        "tables": [
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
                        "size": (1, 1),
                        "type": "INT IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "company_id",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "BIGINT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_last_name",
                        "nullable": False,
                        "references": None,
                        "size": 8000,
                        "type": "VARBINARY",
                        "unique": False,
                    },
                ],
                "index": [],
                "partitioned_by": [],
                "primary_key": ["id"],
                "schema": None,
                "table_name": "sqlserverlist",
                "tablespace": None,
                "constraints": {
                    "uniques": [
                        {
                            "columns": ["company_id", "user_last_name"],
                            "constraint_name": "UC_sqlserverlist_last_name",
                        }
                    ]
                },
            }
        ],
        "types": [],
    }

    assert expected == result


def test_constraint_unique_none():
    ddl = """
    CREATE TABLE sqlserverlist (

    id INT IDENTITY (1,1) PRIMARY KEY, -- NOTE
    company_id BIGINT ,
    user_last_name 	VARBINARY(8000) NOT NULL
    )
    """

    result = DDLParser(ddl).run(group_by_type=True, output_mode="mssql")
    expected = {
        "comments": [" NOTE"],
        "sequences": [],
        "ddl_properties": [],
        "domains": [],
        "schemas": [],
        "tables": [
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
                        "size": (1, 1),
                        "type": "INT IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "company_id",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "BIGINT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_last_name",
                        "nullable": False,
                        "references": None,
                        "size": 8000,
                        "type": "VARBINARY",
                        "unique": False,
                    },
                ],
                "index": [],
                "partitioned_by": [],
                "primary_key": ["id"],
                "schema": None,
                "table_name": "sqlserverlist",
                "tablespace": None,
                "constraints": {"uniques": None, "checks": None, "references": None},
            }
        ],
        "types": [],
    }

    assert expected == result


def test_two_unique_constructs():
    ddl = """
    CREATE TABLE sqlserverlist (

    id INT IDENTITY (1,1) PRIMARY KEY, -- NOTE
    company_id BIGINT ,
    primary_id INT FOREIGN KEY REFERENCES Persons(PersonID), -- ADD THIS COLUMN FOR THE FOREIGN KEY
    age TINYINT NULL UNIQUE,
    days_active SMALLINT NOT NULL,
    user_origin_of_birth char(255),
    user_account VARCHAR(8000) NOT NULL,
    user_first_name VARCHAR(max) NOT NULL,
    user_last_name 	VARBINARY(8000) NOT NULL,
    user_street NCHAR(400) NULL,
    user_city NVARCHAR(4000),
    about_user NTEXT NULL,
    user_description TEXT,
    starting_funds FLOAT(53) NULL,
    extra_funds REAL,
    current_funds DECIMAL (38,20),
    ending_funds SMALLMONEY NOT NULL,
    birth_date DATE NOT NULL,
    time_of_birth TIME(7),
    enrollment_date SMALLDATETIME,
    delete_date DATETIME NULL,
    create_date DATETIME2(7) NOT NULL,
    user_time_zone DATETIMEOFFSET(7),
    oder_date date DEFAULT GETDATE(), -- added to demonstrate sql sever Defaults
    country varchar(255) DEFAULT 'Sandnes', -- added to demonstrate sql sever Defaults
    active bit NULL,
    home_size GEOMETRY, -- Sql Server Defaults to Null
    user_photo IMAGE, -- Sql Server Defaults to Null
    --UNIQUE (id),
    CONSTRAINT UC_date UNIQUE (delete_date,create_date),
    CONSTRAINT UC_sqlserverlist_last_name UNIQUE (company_id,user_last_name),
    CONSTRAINT CHK_Person_Age_under CHECK (days_active<=18 AND user_city='New York'),
    CONSTRAINT FK_Person_Age_under  FOREIGN KEY (id)REFERENCES Persons(PersonID)
    )
    """

    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        'comments': [' NOTE', ' ADD THIS COLUMN FOR THE FOREIGN KEY',
' added to demonstrate sql sever Defaults',
' added to demonstrate sql sever Defaults',
' Sql Server Defaults to Null',
' Sql Server Defaults to Null'],
        "sequences": [],
        "ddl_properties": [],
        "domains": [],
        "schemas": [],
        "tables": [
            {
                "alter": {},
                "checks": [
                    {
                        "constraint_name": "CHK_Person_Age_under",
                        "statement": "days_active<=18 AND user_city= 'New York'",
                    }
                ],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "id",
                        "nullable": False,
                        "references": None,
                        "size": (1, 1),
                        "type": "INT IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "company_id",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "BIGINT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "primary_id",
                        "nullable": True,
                        "references": {
                            "column": "PersonID",
                            "deferrable_initially": None,
                            "on_delete": None,
                            "on_update": None,
                            "schema": None,
                            "table": "Persons",
                        },
                        "size": None,
                        "type": "INT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "age",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "TINYINT",
                        "unique": True,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "days_active",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "SMALLINT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_origin_of_birth",
                        "nullable": True,
                        "references": None,
                        "size": 255,
                        "type": "char",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_account",
                        "nullable": False,
                        "references": None,
                        "size": 8000,
                        "type": "VARCHAR",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_first_name",
                        "nullable": False,
                        "references": None,
                        "size": "max",
                        "type": "VARCHAR",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_last_name",
                        "nullable": False,
                        "references": None,
                        "size": 8000,
                        "type": "VARBINARY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_street",
                        "nullable": True,
                        "references": None,
                        "size": 400,
                        "type": "NCHAR",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_city",
                        "nullable": True,
                        "references": None,
                        "size": 4000,
                        "type": "NVARCHAR",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "about_user",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "NTEXT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_description",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "TEXT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "starting_funds",
                        "nullable": True,
                        "references": None,
                        "size": 53,
                        "type": "FLOAT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "extra_funds",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "REAL",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "current_funds",
                        "nullable": True,
                        "references": None,
                        "size": (38, 20),
                        "type": "DECIMAL",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "ending_funds",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "SMALLMONEY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "birth_date",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "DATE",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "time_of_birth",
                        "nullable": True,
                        "references": None,
                        "size": 7,
                        "type": "TIME",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "enrollment_date",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "SMALLDATETIME",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "delete_date",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "DATETIME",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "create_date",
                        "nullable": False,
                        "references": None,
                        "size": 7,
                        "type": "DATETIME2",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_time_zone",
                        "nullable": True,
                        "references": None,
                        "size": 7,
                        "type": "DATETIMEOFFSET",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": "GETDATE()",
                        "name": "oder_date",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "date",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": "'Sandnes'",
                        "name": "country",
                        "nullable": True,
                        "references": None,
                        "size": 255,
                        "type": "varchar",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "active",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "bit",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "home_size",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "GEOMETRY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_photo",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "IMAGE",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "checks": [
                        {
                            "constraint_name": "CHK_Person_Age_under",
                            "statement": "days_active<=18 AND " "user_city= 'New York'",
                        }
                    ],
                    "references": [
                        {
                            "columns": ["PersonID"],
                            "ref_columns": ["id"],
                            "constraint_name": "FK_Person_Age_under",
                            "deferrable_initially": None,
                            "on_delete": None,
                            "on_update": None,
                            "schema": None,
                            "table": "Persons",
                        }
                    ],
                    "uniques": [
                        {
                            "columns": ["delete_date", "create_date"],
                            "constraint_name": "UC_date",
                        },
                        {
                            "columns": ["company_id", "user_last_name"],
                            "constraint_name": "UC_sqlserverlist_last_name",
                        },
                    ],
                },
                "index": [],
                "partitioned_by": [],
                "primary_key": ["id"],
                "schema": None,
                "table_name": "sqlserverlist",
                "tablespace": None,
            }
        ],
        "types": [],
    }
    assert expected == result


def test_foreign_keys():
    ddl = """

   CREATE TABLE sqlserverlist (

   id INT IDENTITY (1,1) PRIMARY KEY, -- NOTE
   company_id BIGINT ,
   primary_id INT FOREIGN KEY REFERENCES Persons(PersonID), -- ADD THIS COLUMN FOR THE FOREIGN KEY
   age TINYINT NULL UNIQUE,
   days_active SMALLINT NOT NULL,
   user_origin_of_birth char(255),
   user_account VARCHAR(8000) NOT NULL,
   user_first_name VARCHAR(max) NOT NULL,
   user_last_name 	VARBINARY(8000) NOT NULL,
   user_street NCHAR(400) NULL,
   user_city NVARCHAR(4000),
   about_user NTEXT NULL,
   user_description TEXT,
   starting_funds FLOAT(53) NULL,
   extra_funds REAL,
   current_funds DECIMAL (38,20),
   ending_funds SMALLMONEY NOT NULL,
   birth_date DATE NOT NULL,
   time_of_birth TIME(7),
   oder_date date DEFAULT GETDATE(), -- added to demonstrate sql sever Defaults
   country varchar(255) DEFAULT 'Sandnes', -- added to demonstrate sql sever Defaults
   active bit NULL,
   home_size GEOMETRY, -- Sql Server Defaults to Null
   user_photo IMAGE, -- Sql Server Defaults to Null
   --UNIQUE (id),
   CONSTRAINT UC_sqlserverlist_last_name UNIQUE (company_id,user_last_name),
   CONSTRAINT CHK_Person_Age_under CHECK (days_active<=18 AND user_city='New York'),
   FOREIGN KEY (id) REFERENCES Persons(PersonID),
   FOREIGN KEY (user_first_name, id) REFERENCES Persons(PersonID, PersonName),
   );
   """

    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        'comments': [' NOTE', ' ADD THIS COLUMN FOR THE FOREIGN KEY',
' added to demonstrate sql sever Defaults',
' added to demonstrate sql sever Defaults',
' Sql Server Defaults to Null',
' Sql Server Defaults to Null'],
        "sequences": [],
        "domains": [],
        "schemas": [],
        "tables": [
            {
                "alter": {},
                "checks": [
                    {
                        "constraint_name": "CHK_Person_Age_under",
                        "statement": "days_active<=18 AND user_city= 'New York'",
                    }
                ],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "id",
                        "nullable": False,
                        "references": {
                            "column": "PersonName",
                            "deferrable_initially": None,
                            "on_delete": None,
                            "on_update": None,
                            "schema": None,
                            "table": "Persons",
                        },
                        "size": (1, 1),
                        "type": "INT IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "company_id",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "BIGINT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "primary_id",
                        "nullable": True,
                        "references": {
                            "column": "PersonID",
                            "deferrable_initially": None,
                            "on_delete": None,
                            "on_update": None,
                            "schema": None,
                            "table": "Persons",
                        },
                        "size": None,
                        "type": "INT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "age",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "TINYINT",
                        "unique": True,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "days_active",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "SMALLINT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_origin_of_birth",
                        "nullable": True,
                        "references": None,
                        "size": 255,
                        "type": "char",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_account",
                        "nullable": False,
                        "references": None,
                        "size": 8000,
                        "type": "VARCHAR",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_first_name",
                        "nullable": False,
                        "references": {
                            "column": "PersonID",
                            "deferrable_initially": None,
                            "on_delete": None,
                            "on_update": None,
                            "schema": None,
                            "table": "Persons",
                        },
                        "size": "max",
                        "type": "VARCHAR",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_last_name",
                        "nullable": False,
                        "references": None,
                        "size": 8000,
                        "type": "VARBINARY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_street",
                        "nullable": True,
                        "references": None,
                        "size": 400,
                        "type": "NCHAR",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_city",
                        "nullable": True,
                        "references": None,
                        "size": 4000,
                        "type": "NVARCHAR",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "about_user",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "NTEXT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_description",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "TEXT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "starting_funds",
                        "nullable": True,
                        "references": None,
                        "size": 53,
                        "type": "FLOAT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "extra_funds",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "REAL",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "current_funds",
                        "nullable": True,
                        "references": None,
                        "size": (38, 20),
                        "type": "DECIMAL",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "ending_funds",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "SMALLMONEY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "birth_date",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "DATE",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "time_of_birth",
                        "nullable": True,
                        "references": None,
                        "size": 7,
                        "type": "TIME",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": "GETDATE()",
                        "name": "oder_date",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "date",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": "'Sandnes'",
                        "name": "country",
                        "nullable": True,
                        "references": None,
                        "size": 255,
                        "type": "varchar",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "active",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "bit",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "home_size",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "GEOMETRY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_photo",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "IMAGE",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "checks": [
                        {
                            "constraint_name": "CHK_Person_Age_under",
                            "statement": "days_active<=18 AND " "user_city= 'New York'",
                        }
                    ],
                    "uniques": [
                        {
                            "columns": ["company_id", "user_last_name"],
                            "constraint_name": "UC_sqlserverlist_last_name",
                        }
                    ],
                },
                "index": [],
                "partitioned_by": [],
                "primary_key": ["id"],
                "schema": None,
                "table_name": "sqlserverlist",
                "tablespace": None,
            }
        ],
        "types": [],
        "ddl_properties": [],
    }
    assert expected == result


def test_alter_unique():
    ddl = """
   CREATE TABLE sqlserverlist (

   id INT IDENTITY (1,1) PRIMARY KEY, -- NOTE
   company_id BIGINT ,
   primary_id INT FOREIGN KEY REFERENCES Persons(PersonID), -- ADD THIS COLUMN FOR THE FOREIGN KEY
   age TINYINT NULL UNIQUE,
   days_active SMALLINT NOT NULL,
   user_origin_of_birth char(255),
   user_account VARCHAR(8000) NOT NULL,
   user_first_name VARCHAR(max) NOT NULL,
   user_last_name 	VARBINARY(8000) NOT NULL,
   user_street NCHAR(400) NULL,
   user_city NVARCHAR(4000),
   about_user NTEXT NULL,
   user_description TEXT,
   starting_funds FLOAT(53) NULL,
   extra_funds REAL,
   current_funds DECIMAL (38,20),
   ending_funds SMALLMONEY NOT NULL,
   birth_date DATE NOT NULL,
   time_of_birth TIME(7),
   enrollment_date SMALLDATETIME,
   delete_date DATETIME NULL,
   create_date DATETIME2(7) NOT NULL,
   user_time_zone DATETIMEOFFSET(7),
   oder_date date DEFAULT GETDATE(), -- added to demonstrate sql sever Defaults
   country varchar(255) DEFAULT 'Sandnes', -- added to demonstrate sql sever Defaults
   active bit NULL,
   home_size GEOMETRY, -- Sql Server Defaults to Null
   user_photo IMAGE, -- Sql Server Defaults to Null
   --UNIQUE (id),
   CONSTRAINT UC_sqlserverlist_last_name UNIQUE (company_id,user_last_name),
   CONSTRAINT CHK_Person_Age_under CHECK (days_active<=18 AND user_city='New York'),
   FOREIGN KEY (id) REFERENCES Persons(PersonID),
   CONSTRAINT FK_Person_Age_under  FOREIGN KEY (id)REFERENCES Persons(PersonID)
   );
   -- UNIQUE CONSTRAINTS
   ALTER TABLE sqlserverlist ADD UNIQUE (birth_date);
   ALTER TABLE sqlserverlist ADD CONSTRAINT UC_Person_ening_funds UNIQUE (current_funds,create_date);
   """

    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        'comments': [' NOTE', ' ADD THIS COLUMN FOR THE FOREIGN KEY',
' added to demonstrate sql sever Defaults',
' added to demonstrate sql sever Defaults',
' Sql Server Defaults to Null',
' Sql Server Defaults to Null'],
        "sequences": [],
        "ddl_properties": [],
        "domains": [],
        "schemas": [],
        "tables": [
            {
                "alter": {
                    "uniques": [
                        {"columns": ["birth_date"], "constraint_name": None},
                        {
                            "columns": ["current_funds", "create_date"],
                            "constraint_name": "UC_Person_ening_funds",
                        },
                    ]
                },
                "checks": [
                    {
                        "constraint_name": "CHK_Person_Age_under",
                        "statement": "days_active<=18 AND user_city= 'New York'",
                    }
                ],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "id",
                        "nullable": False,
                        "references": {
                            "column": "PersonID",
                            "deferrable_initially": None,
                            "on_delete": None,
                            "on_update": None,
                            "schema": None,
                            "table": "Persons",
                        },
                        "size": (1, 1),
                        "type": "INT IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "company_id",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "BIGINT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "primary_id",
                        "nullable": True,
                        "references": {
                            "column": "PersonID",
                            "deferrable_initially": None,
                            "on_delete": None,
                            "on_update": None,
                            "schema": None,
                            "table": "Persons",
                        },
                        "size": None,
                        "type": "INT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "age",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "TINYINT",
                        "unique": True,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "days_active",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "SMALLINT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_origin_of_birth",
                        "nullable": True,
                        "references": None,
                        "size": 255,
                        "type": "char",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_account",
                        "nullable": False,
                        "references": None,
                        "size": 8000,
                        "type": "VARCHAR",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_first_name",
                        "nullable": False,
                        "references": None,
                        "size": "max",
                        "type": "VARCHAR",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_last_name",
                        "nullable": False,
                        "references": None,
                        "size": 8000,
                        "type": "VARBINARY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_street",
                        "nullable": True,
                        "references": None,
                        "size": 400,
                        "type": "NCHAR",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_city",
                        "nullable": True,
                        "references": None,
                        "size": 4000,
                        "type": "NVARCHAR",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "about_user",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "NTEXT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_description",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "TEXT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "starting_funds",
                        "nullable": True,
                        "references": None,
                        "size": 53,
                        "type": "FLOAT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "extra_funds",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "REAL",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "current_funds",
                        "nullable": True,
                        "references": None,
                        "size": (38, 20),
                        "type": "DECIMAL",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "ending_funds",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "SMALLMONEY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "birth_date",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "DATE",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "time_of_birth",
                        "nullable": True,
                        "references": None,
                        "size": 7,
                        "type": "TIME",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "enrollment_date",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "SMALLDATETIME",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "delete_date",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "DATETIME",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "create_date",
                        "nullable": False,
                        "references": None,
                        "size": 7,
                        "type": "DATETIME2",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_time_zone",
                        "nullable": True,
                        "references": None,
                        "size": 7,
                        "type": "DATETIMEOFFSET",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": "GETDATE()",
                        "name": "oder_date",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "date",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": "'Sandnes'",
                        "name": "country",
                        "nullable": True,
                        "references": None,
                        "size": 255,
                        "type": "varchar",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "active",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "bit",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "home_size",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "GEOMETRY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_photo",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "IMAGE",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "checks": [
                        {
                            "constraint_name": "CHK_Person_Age_under",
                            "statement": "days_active<=18 AND " "user_city= 'New York'",
                        }
                    ],
                    "references": [
                        {
                            "columns": ["PersonID"],
                            "ref_columns": ["id"],
                            "constraint_name": "FK_Person_Age_under",
                            "deferrable_initially": None,
                            "on_delete": None,
                            "on_update": None,
                            "schema": None,
                            "table": "Persons",
                        }
                    ],
                    "uniques": [
                        {
                            "columns": ["company_id", "user_last_name"],
                            "constraint_name": "UC_sqlserverlist_last_name",
                        }
                    ],
                },
                "index": [],
                "partitioned_by": [],
                "primary_key": ["id"],
                "schema": None,
                "table_name": "sqlserverlist",
                "tablespace": None,
            }
        ],
        "types": [],
    }
    assert expected == result


def test_defaults_in_alter():
    ddl = """

    CREATE TABLE sqlserverlist (

    id INT IDENTITY (1,1) PRIMARY KEY, -- NOTE
    company_id BIGINT ,
    primary_id INT FOREIGN KEY REFERENCES Persons(PersonID), -- ADD THIS COLUMN FOR THE FOREIGN KEY
    age TINYINT NULL UNIQUE,
    days_active SMALLINT NOT NULL,
    user_origin_of_birth char(255),
    user_account VARCHAR(8000) NOT NULL,
    user_time_zone DATETIMEOFFSET(7),
    oder_date date DEFAULT GETDATE(), -- added to demonstrate sql sever Defaults
    country varchar(255) DEFAULT 'Sandnes', -- added to demonstrate sql sever Defaults
    active bit NULL,
    home_size GEOMETRY, -- Sql Server Defaults to Null
    user_photo IMAGE, -- Sql Server Defaults to Null
    --UNIQUE (id),
    CONSTRAINT UC_sqlserverlist_last_name UNIQUE (company_id,user_last_name),
    CONSTRAINT CHK_Person_Age_under CHECK (days_active<=18 AND user_city='New York'),
    FOREIGN KEY (id) REFERENCES Persons(PersonID),
    CONSTRAINT FK_Person_Age_under  FOREIGN KEY (id)REFERENCES Persons(PersonID)
    );

    ALTER TABLE sqlserverlist ADD CONSTRAINT df_user_street DEFAULT '1 WAY STREET' FOR user_street;
    """

    result = DDLParser(ddl).run(group_by_type=True, output_mode="mssql")
    expected = {
        'comments': [' NOTE', ' ADD THIS COLUMN FOR THE FOREIGN KEY',
' added to demonstrate sql sever Defaults',
' added to demonstrate sql sever Defaults',
' Sql Server Defaults to Null',
' Sql Server Defaults to Null'],
        "sequences": [],
        "ddl_properties": [],
        "domains": [],
        "schemas": [],
        "tables": [
            {
                "alter": {
                    "defaults": [
                        {
                            "columns": ["user_street"],
                            "constraint_name": "df_user_street",
                            "value": "'1 WAY STREET'",
                        }
                    ]
                },
                "checks": [
                    {
                        "constraint_name": "CHK_Person_Age_under",
                        "statement": "days_active<=18 AND user_city= 'New York'",
                    }
                ],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "id",
                        "nullable": False,
                        "references": {
                            "column": "PersonID",
                            "deferrable_initially": None,
                            "on_delete": None,
                            "on_update": None,
                            "schema": None,
                            "table": "Persons",
                        },
                        "size": (1, 1),
                        "type": "INT IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "company_id",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "BIGINT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "primary_id",
                        "nullable": True,
                        "references": {
                            "column": "PersonID",
                            "deferrable_initially": None,
                            "on_delete": None,
                            "on_update": None,
                            "schema": None,
                            "table": "Persons",
                        },
                        "size": None,
                        "type": "INT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "age",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "TINYINT",
                        "unique": True,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "days_active",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "SMALLINT",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_origin_of_birth",
                        "nullable": True,
                        "references": None,
                        "size": 255,
                        "type": "char",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_account",
                        "nullable": False,
                        "references": None,
                        "size": 8000,
                        "type": "VARCHAR",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_time_zone",
                        "nullable": True,
                        "references": None,
                        "size": 7,
                        "type": "DATETIMEOFFSET",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": "GETDATE()",
                        "name": "oder_date",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "date",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": "'Sandnes'",
                        "name": "country",
                        "nullable": True,
                        "references": None,
                        "size": 255,
                        "type": "varchar",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "active",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "bit",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "home_size",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "GEOMETRY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "user_photo",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "IMAGE",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "checks": [
                        {
                            "constraint_name": "CHK_Person_Age_under",
                            "statement": "days_active<=18 AND " "user_city= 'New York'",
                        }
                    ],
                    "references": [
                        {
                            "columns": ["PersonID"],
                            "ref_columns": ["id"],
                            "constraint_name": "FK_Person_Age_under",
                            "deferrable_initially": None,
                            "on_delete": None,
                            "on_update": None,
                            "schema": None,
                            "table": "Persons",
                        }
                    ],
                    "uniques": [
                        {
                            "columns": ["company_id", "user_last_name"],
                            "constraint_name": "UC_sqlserverlist_last_name",
                        }
                    ],
                },
                "index": [],
                "partitioned_by": [],
                "primary_key": ["id"],
                "schema": None,
                "table_name": "sqlserverlist",
                "tablespace": None,
            }
        ],
        "types": [],
    }
    assert expected == result


def test_mysql_constraint_pk():
    ddl = """

    CREATE TABLE Persons (
        ID int NOT NULL,
        LastName varchar(255) NOT NULL,
        FirstName varchar(255),
        Age int,
        CONSTRAINT PK_Person PRIMARY KEY (ID,LastName)
    );
    """

    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        "sequences": [],
        "ddl_properties": [],
        "domains": [],
        "schemas": [],
        "tables": [
            {
                "alter": {},
                "checks": [],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "ID",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "int",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "LastName",
                        "nullable": False,
                        "references": None,
                        "size": 255,
                        "type": "varchar",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "FirstName",
                        "nullable": True,
                        "references": None,
                        "size": 255,
                        "type": "varchar",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "Age",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "int",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "primary_keys": [
                        {"columns": ["ID", "LastName"], "constraint_name": "PK_Person"}
                    ]
                },
                "index": [],
                "partitioned_by": [],
                "primary_key": ["ID", "LastName"],
                "schema": None,
                "table_name": "Persons",
                "tablespace": None,
            }
        ],
        "types": [],
    }
    assert expected == result


def test_constraint_primary_key():
    expected = {
        "ddl_properties": [],
        "domains": [],
        "schemas": [],
        "sequences": [],
        "tables": [
            {
                "alter": {},
                "checks": [],
                "clustered_primary_key": [{"column": "[id]", "order": "ASC"}],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "[id]",
                        "nullable": False,
                        "references": None,
                        "size": (1, 1),
                        "type": "[int] IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[user_id]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[int]",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "primary_keys": [
                        {
                            "columns": ["[id]"],
                            "detailed_columns": [{"column": "[id]", "order": "ASC"}],
                            "constraint_name": "[PK_users_WorkSchedule_id]",
                        },
                        {
                            "columns": ["[id]"],
                            "detailed_columns": [{"column": "[id]", "order": "ASC"}],
                            "constraint_name": "[PK_users_WorkSchedule_id]",
                        },
                    ]
                },
                "index": [],
                "partitioned_by": [],
                "primary_key": ["[id]"],
                "schema": "[dbo]",
                "table_name": "[users_WorkSchedule]",
                "tablespace": None,
            }
        ],
        "types": [],
    }

    ddl = """CREATE TABLE [dbo].[users_WorkSchedule](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [user_id] [int] NULL),
        CONSTRAINT [PK_users_WorkSchedule_id] PRIMARY KEY CLUSTERED
    (
        [id] ASC
    ),

        CONSTRAINT [PK_users_WorkSchedule_id] PRIMARY KEY
    (
        [id] ASC
    )
    """
    result = DDLParser(ddl).run(group_by_type=True)
    assert result == expected


def test_constraint_with_with():
    ddl = """
    USE [mystaffonline]
    GO
    /****** Object:  Table [dbo].[users_WorkSchedule]    Script Date: 9/29/2021 9:55:26 PM ******/
    SET ANSI_NULLS ON
    GO
    SET QUOTED_IDENTIFIER ON
    GO
    CREATE TABLE [dbo].[users_WorkSchedule](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [RequestDropDate] [smalldatetime] NULL,
        [ShiftClass] [varchar](5) NULL,
        [StartHistory] [datetime2](7) GENERATED ALWAYS AS ROW START NOT NULL,
        [EndHistory] [datetime2](7) GENERATED ALWAYS AS ROW END NOT NULL,
        CONSTRAINT [PK_users_WorkSchedule_id] PRIMARY KEY CLUSTERED
        (
        [id] ASC
    )
    WITH (PAD_INDEX = OFF,
        STATISTICS_NORECOMPUTE = OFF,
        IGNORE_DUP_KEY = OFF,
        ALLOW_ROW_LOCKS = ON,
        ALLOW_PAGE_LOCKS = ON))"""
    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        "comments": [
            "***** Object:  Table [dbo].[users_WorkSchedule]    Script Date: "
            "9/29/2021 9:55:26 PM ******/"
        ],
        "ddl_properties": [
            {"name": "ANSI_NULLS", "value": "ON"},
            {"name": "QUOTED_IDENTIFIER", "value": "ON"},
        ],
        "domains": [],
        "schemas": [],
        "sequences": [],
        "tables": [
            {
                "alter": {},
                "checks": [],
                "clustered_primary_key": [{"column": "[id]", "order": "ASC"}],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "[id]",
                        "nullable": False,
                        "references": None,
                        "size": (1, 1),
                        "type": "[int] IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[RequestDropDate]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[smalldatetime]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[ShiftClass]",
                        "nullable": True,
                        "references": None,
                        "size": 5,
                        "type": "[varchar]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "generated": {
                            "always": True,
                            "as": "ROW START",
                            "stored": False,
                        },
                        "name": "[StartHistory]",
                        "nullable": False,
                        "references": None,
                        "size": 7,
                        "type": "[datetime2]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "generated": {"always": True, "as": "ROW END", "stored": False},
                        "name": "[EndHistory]",
                        "nullable": False,
                        "references": None,
                        "size": 7,
                        "type": "[datetime2]",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "primary_keys": [
                        {
                            "columns": ["[id]"],
                            "detailed_columns": [{"column": "[id]", "order": "ASC"}],
                            "constraint_name": "[PK_users_WorkSchedule_id]",
                        }
                    ]
                },
                "index": [],
                "partitioned_by": [],
                "primary_key": ["[id]"],
                "schema": "[dbo]",
                "table_name": "[users_WorkSchedule]",
                "tablespace": None,
                "with": {
                    "on": None,
                    "properties": [
                        {"name": "PAD_INDEX", "value": "OFF"},
                        {"name": "STATISTICS_NORECOMPUTE", "value": "OFF"},
                        {"name": "IGNORE_DUP_KEY", "value": "OFF"},
                        {"name": "ALLOW_ROW_LOCKS", "value": "ON"},
                        {"name": "ALLOW_PAGE_LOCKS", "value": "ON"},
                    ],
                },
            }
        ],
        "types": [],
    }
    assert expected == result


def test_with_on():
    expected = {
        "ddl_properties": [],
        "domains": [],
        "schemas": [],
        "sequences": [],
        "tables": [
            {
                "alter": {},
                "checks": [],
                "clustered_primary_key": [{"column": "[id]", "order": "ASC"}],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "[id]",
                        "nullable": False,
                        "references": None,
                        "size": (1, 1),
                        "type": "[int] IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[RequestDropDate]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[smalldatetime]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[ShiftClass]",
                        "nullable": True,
                        "references": None,
                        "size": 5,
                        "type": "[varchar]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "generated": {
                            "always": True,
                            "as": "ROW START",
                            "stored": False,
                        },
                        "name": "[StartHistory]",
                        "nullable": False,
                        "references": None,
                        "size": 7,
                        "type": "[datetime2]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "generated": {"always": True, "as": "ROW END", "stored": False},
                        "name": "[EndHistory]",
                        "nullable": False,
                        "references": None,
                        "size": 7,
                        "type": "[datetime2]",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "primary_keys": [
                        {
                            "columns": ["[id]"],
                            "detailed_columns": [{"column": "[id]", "order": "ASC"}],
                            "constraint_name": "[PK_users_WorkSchedule_id]",
                        }
                    ]
                },
                "index": [],
                "on": "[PRIMARY]",
                "partitioned_by": [],
                "primary_key": ["[id]"],
                "schema": "[dbo]",
                "table_name": "[users_WorkSchedule]",
                "tablespace": None,
                "with": {
                    "on": None,
                    "properties": [
                        {"name": "PAD_INDEX", "value": "OFF"},
                        {"name": "STATISTICS_NORECOMPUTE", "value": "OFF"},
                        {"name": "IGNORE_DUP_KEY", "value": "OFF"},
                        {"name": "ALLOW_ROW_LOCKS", "value": "ON"},
                        {"name": "ALLOW_PAGE_LOCKS", "value": "ON"},
                    ],
                },
            }
        ],
        "types": [],
    }
    ddl = """CREATE TABLE [dbo].[users_WorkSchedule](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [RequestDropDate] [smalldatetime] NULL,
        [ShiftClass] [varchar](5) NULL,
        [StartHistory] [datetime2](7) GENERATED ALWAYS AS ROW START NOT NULL,
        [EndHistory] [datetime2](7) GENERATED ALWAYS AS ROW END NOT NULL,
        CONSTRAINT [PK_users_WorkSchedule_id] PRIMARY KEY CLUSTERED
        (
            [id] ASC
        )
        WITH (
            PAD_INDEX = OFF,
            STATISTICS_NORECOMPUTE = OFF,
            IGNORE_DUP_KEY = OFF,
            ALLOW_ROW_LOCKS = ON,
            ALLOW_PAGE_LOCKS = ON
        )  ON [PRIMARY]
    )"""
    result = DDLParser(ddl).run(group_by_type=True)
    assert expected == result


def test_period_for_system_time():
    ddl = """CREATE TABLE [dbo].[users_WorkSchedule](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [RequestDropDate] [smalldatetime] NULL,
        [ShiftClass] [varchar](5) NULL,
        [StartHistory] [datetime2](7) GENERATED ALWAYS AS ROW START NOT NULL,
        [EndHistory] [datetime2](7) GENERATED ALWAYS AS ROW END NOT NULL,
        CONSTRAINT [PK_users_WorkSchedule_id] PRIMARY KEY CLUSTERED
        (
            [id] ASC
        )
        WITH (
            PAD_INDEX = OFF,
            STATISTICS_NORECOMPUTE = OFF,
            IGNORE_DUP_KEY = OFF,
            ALLOW_ROW_LOCKS = ON,
            ALLOW_PAGE_LOCKS = ON
        )  ON [PRIMARY],
        PERIOD FOR SYSTEM_TIME ([StartHistory], [EndHistory])
    )
  """
    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        "ddl_properties": [],
        "domains": [],
        "schemas": [],
        "sequences": [],
        "tables": [
            {
                "alter": {},
                "checks": [],
                "clustered_primary_key": [{"column": "[id]", "order": "ASC"}],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "[id]",
                        "nullable": False,
                        "references": None,
                        "size": (1, 1),
                        "type": "[int] IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[RequestDropDate]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[smalldatetime]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[ShiftClass]",
                        "nullable": True,
                        "references": None,
                        "size": 5,
                        "type": "[varchar]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "generated": {
                            "always": True,
                            "as": "ROW START",
                            "stored": False,
                        },
                        "name": "[StartHistory]",
                        "nullable": False,
                        "references": None,
                        "size": 7,
                        "type": "[datetime2]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "generated": {"always": True, "as": "ROW END", "stored": False},
                        "name": "[EndHistory]",
                        "nullable": False,
                        "references": None,
                        "size": 7,
                        "type": "[datetime2]",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "primary_keys": [
                        {
                            "columns": ["[id]"],
                            "detailed_columns": [{"column": "[id]", "order": "ASC"}],
                            "constraint_name": "[PK_users_WorkSchedule_id]",
                        }
                    ]
                },
                "index": [],
                "on": "[PRIMARY]",
                "partitioned_by": [],
                "period_for_system_time": ["[StartHistory]", "[EndHistory]"],
                "primary_key": ["[id]"],
                "schema": "[dbo]",
                "table_name": "[users_WorkSchedule]",
                "tablespace": None,
                "with": {
                    "on": None,
                    "properties": [
                        {"name": "PAD_INDEX", "value": "OFF"},
                        {"name": "STATISTICS_NORECOMPUTE", "value": "OFF"},
                        {"name": "IGNORE_DUP_KEY", "value": "OFF"},
                        {"name": "ALLOW_ROW_LOCKS", "value": "ON"},
                        {"name": "ALLOW_PAGE_LOCKS", "value": "ON"},
                    ],
                },
            }
        ],
        "types": [],
    }
    assert expected == result


def test_on_primary_on_table_level():

    ddl = """CREATE TABLE [dbo].[users_WorkSchedule](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [RequestDropDate] [smalldatetime] NULL,
        [ShiftClass] [varchar](5) NULL,
        [StartHistory] [datetime2](7) GENERATED ALWAYS AS ROW START NOT NULL,
        [EndHistory] [datetime2](7) GENERATED ALWAYS AS ROW END NOT NULL,
        CONSTRAINT [PK_users_WorkSchedule_id] PRIMARY KEY CLUSTERED
        (
            [id] ASC
        )
        WITH (
            PAD_INDEX = OFF,
            STATISTICS_NORECOMPUTE = OFF,
            IGNORE_DUP_KEY = OFF,
            ALLOW_ROW_LOCKS = ON,
            ALLOW_PAGE_LOCKS = ON
        )  ON [PRIMARY],
        PERIOD FOR SYSTEM_TIME ([StartHistory], [EndHistory])
    )) ON [PRIMARY]
  """
    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        "ddl_properties": [],
        "domains": [],
        "schemas": [],
        "sequences": [],
        "tables": [
            {
                "alter": {},
                "checks": [],
                "clustered_primary_key": [{"column": "[id]", "order": "ASC"}],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "[id]",
                        "nullable": False,
                        "references": None,
                        "size": (1, 1),
                        "type": "[int] IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[RequestDropDate]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[smalldatetime]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[ShiftClass]",
                        "nullable": True,
                        "references": None,
                        "size": 5,
                        "type": "[varchar]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "generated": {
                            "always": True,
                            "as": "ROW START",
                            "stored": False,
                        },
                        "name": "[StartHistory]",
                        "nullable": False,
                        "references": None,
                        "size": 7,
                        "type": "[datetime2]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "generated": {"always": True, "as": "ROW END", "stored": False},
                        "name": "[EndHistory]",
                        "nullable": False,
                        "references": None,
                        "size": 7,
                        "type": "[datetime2]",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "primary_keys": [
                        {
                            "columns": ["[id]"],
                            "detailed_columns": [{"column": "[id]", "order": "ASC"}],
                            "constraint_name": "[PK_users_WorkSchedule_id]",
                        }
                    ]
                },
                "index": [],
                "on": "[PRIMARY]",
                "partitioned_by": [],
                "period_for_system_time": ["[StartHistory]", "[EndHistory]"],
                "primary_key": ["[id]"],
                "schema": "[dbo]",
                "table_name": "[users_WorkSchedule]",
                "tablespace": None,
                "with": {
                    "on": None,
                    "properties": [
                        {"name": "PAD_INDEX", "value": "OFF"},
                        {"name": "STATISTICS_NORECOMPUTE", "value": "OFF"},
                        {"name": "IGNORE_DUP_KEY", "value": "OFF"},
                        {"name": "ALLOW_ROW_LOCKS", "value": "ON"},
                        {"name": "ALLOW_PAGE_LOCKS", "value": "ON"},
                    ],
                },
            }
        ],
        "types": [],
    }
    assert expected == result


def test_with_on_table_level():

    ddl = """USE [mystaffonline]
    GO
    /****** Object:  Table [dbo].[users_WorkSchedule]    Script Date: 9/29/2021 9:55:26 PM ******/
    SET ANSI_NULLS ON
    GO
    SET QUOTED_IDENTIFIER ON
    GO
    CREATE TABLE [dbo].[users_WorkSchedule](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [user_id] [int] NULL,
    CONSTRAINT [PK_users_WorkSchedule_id] PRIMARY KEY CLUSTERED
    (
        [id] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF,
    ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
        PERIOD FOR SYSTEM_TIME ([StartHistory], [EndHistory])
    ) ON [PRIMARY]
    WITH
    (
    SYSTEM_VERSIONING = ON
    )"""
    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        "comments": [
            "***** Object:  Table [dbo].[users_WorkSchedule]    Script Date: "
            "9/29/2021 9:55:26 PM ******/"
        ],
        "ddl_properties": [
            {"name": "ANSI_NULLS", "value": "ON"},
            {"name": "QUOTED_IDENTIFIER", "value": "ON"},
        ],
        "domains": [],
        "schemas": [],
        "sequences": [],
        "tables": [
            {
                "alter": {},
                "checks": [],
                "clustered_primary_key": [{"column": "[id]", "order": "ASC"}],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "[id]",
                        "nullable": False,
                        "references": None,
                        "size": (1, 1),
                        "type": "[int] IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[user_id]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[int]",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "primary_keys": [
                        {
                            "columns": ["[id]"],
                            "detailed_columns": [{"column": "[id]", "order": "ASC"}],
                            "constraint_name": "[PK_users_WorkSchedule_id]",
                        }
                    ]
                },
                "index": [],
                "on": "[PRIMARY]",
                "partitioned_by": [],
                "period_for_system_time": ["[StartHistory]", "[EndHistory]"],
                "primary_key": ["[id]"],
                "schema": "[dbo]",
                "table_name": "[users_WorkSchedule]",
                "tablespace": None,
                "with": {
                    "on": None,
                    "properties": [{"name": "SYSTEM_VERSIONING", "value": "ON"}],
                },
            }
        ],
        "types": [],
    }
    assert expected == result


def test_with_on_with_properties():

    ddl = """USE [mystaffonline]
GO
/****** Object:  Table [dbo].[users_WorkSchedule]    Script Date: 9/29/2021 9:55:26 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[users_WorkSchedule](
    [id] [int] IDENTITY(1,1) NOT NULL,
    [user_id] [int] NULL,
    [station_Id] [int] NULL,
 CONSTRAINT [PK_users_WorkSchedule_id] PRIMARY KEY CLUSTERED
(
    [id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF,
ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
    PERIOD FOR SYSTEM_TIME ([StartHistory], [EndHistory])
) ON [PRIMARY]
WITH
(
SYSTEM_VERSIONING = ON ( HISTORY_TABLE = [dbo].[users_WorkScheduleHistory] )
)"""
    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        "comments": [
            "***** Object:  Table [dbo].[users_WorkSchedule]    Script Date: "
            "9/29/2021 9:55:26 PM ******/"
        ],
        "ddl_properties": [
            {"name": "ANSI_NULLS", "value": "ON"},
            {"name": "QUOTED_IDENTIFIER", "value": "ON"},
        ],
        "domains": [],
        "schemas": [],
        "sequences": [],
        "tables": [
            {
                "alter": {},
                "checks": [],
                "clustered_primary_key": [{"column": "[id]", "order": "ASC"}],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "[id]",
                        "nullable": False,
                        "references": None,
                        "size": (1, 1),
                        "type": "[int] IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[user_id]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[int]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[station_Id]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[int]",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "primary_keys": [
                        {
                            "columns": ["[id]"],
                            "detailed_columns": [{"column": "[id]", "order": "ASC"}],
                            "constraint_name": "[PK_users_WorkSchedule_id]",
                        }
                    ]
                },
                "index": [],
                "on": "[PRIMARY]",
                "partitioned_by": [],
                "period_for_system_time": ["[StartHistory]", "[EndHistory]"],
                "primary_key": ["[id]"],
                "schema": "[dbo]",
                "table_name": "[users_WorkSchedule]",
                "tablespace": None,
                "with": {
                    "on": None,
                    "properties": [
                        {"name": "SYSTEM_VERSIONING", "value": "ON"},
                        {
                            "properties": [
                                {
                                    "name": "HISTORY_TABLE",
                                    "value": "[dbo].[users_WorkScheduleHistory]",
                                }
                            ]
                        },
                    ],
                },
            }
        ],
        "types": [],
    }
    assert expected == result


def test_output_separated_by_go_and_textimage():

    ddl = """/****** Object:  Table [dbo].[TO_Requests]    Script Date: 9/29/2021 9:55:26 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TO_Requests](
    [Request_ID] [int] IDENTITY(1,1) NOT NULL,
    [user_id] [int] NULL,
    [date_from] [smalldatetime] NULL,
    [date_to] [smalldatetime] NULL,
    [comments] [varchar](2000) NULL,
    [status] [varchar](10) NOT NULL,
    [profile_id] [int] NULL,
    [DateAdded] [smalldatetime] NOT NULL,
    [UpdatedBy] [int] NULL,
    [UpdatedOn] [smalldatetime] NULL,
    [InitialResponseBy] [int] NULL,
    [InitialResponseDate] [smalldatetime] NULL,
    [InitialResponseStatus] [varchar](10) NULL,
    [adpRequestId] [varchar](50) NULL,
 CONSTRAINT [PK_TO_Requests_Request_ID] PRIMARY KEY CLUSTERED
(
    [Request_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF,
ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ToDo]    Script Date: 9/29/2021 9:55:26 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ToDo](
    [ID] [int] IDENTITY(1,1) NOT NULL,
    [ProfileID] [int] NOT NULL,
    [Title] [varchar](50) NULL,
 CONSTRAINT [PK_ToDo_ID] PRIMARY KEY CLUSTERED
(
    [ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF,
ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ToDoComments]    Script Date: 9/29/2021 9:55:26 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ToDoComments](
    [ToDoCommentsId] [int] IDENTITY(1,1) NOT NULL,
    [CreatedBy] [int] NOT NULL,
 CONSTRAINT [PK_ToDoComments_ToDoCommentsId] PRIMARY KEY CLUSTERED
(
    [ToDoCommentsId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF,
ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO"""
    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        'comments': ['***** Object:  Table [dbo].[TO_Requests]    Script Date: '
'9/29/2021 9:55:26 PM ******/',
'***** Object:  Table [dbo].[ToDo]    Script Date: 9/29/2021 '
'9:55:26 PM ******/',
'***** Object:  Table [dbo].[ToDoComments]    Script Date: '
'9/29/2021 9:55:26 PM ******/'],
        "ddl_properties": [
            {"name": "ANSI_NULLS", "value": "ON"},
            {"name": "QUOTED_IDENTIFIER", "value": "ON"},
            {"name": "ANSI_NULLS", "value": "ON"},
            {"name": "QUOTED_IDENTIFIER", "value": "ON"},
            {"name": "ANSI_NULLS", "value": "ON"},
            {"name": "QUOTED_IDENTIFIER", "value": "ON"},
        ],
        "domains": [],
        "schemas": [],
        "sequences": [],
        "tables": [
            {
                "alter": {},
                "checks": [],
                "clustered_primary_key": [{"column": "[Request_ID]", "order": "ASC"}],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "[Request_ID]",
                        "nullable": False,
                        "references": None,
                        "size": (1, 1),
                        "type": "[int] IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[user_id]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[int]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[date_from]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[smalldatetime]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[date_to]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[smalldatetime]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[comments]",
                        "nullable": True,
                        "references": None,
                        "size": 2000,
                        "type": "[varchar]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[status]",
                        "nullable": False,
                        "references": None,
                        "size": 10,
                        "type": "[varchar]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[profile_id]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[int]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[DateAdded]",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "[smalldatetime]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[UpdatedBy]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[int]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[UpdatedOn]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[smalldatetime]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[InitialResponseBy]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[int]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[InitialResponseDate]",
                        "nullable": True,
                        "references": None,
                        "size": None,
                        "type": "[smalldatetime]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[InitialResponseStatus]",
                        "nullable": True,
                        "references": None,
                        "size": 10,
                        "type": "[varchar]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[adpRequestId]",
                        "nullable": True,
                        "references": None,
                        "size": 50,
                        "type": "[varchar]",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "primary_keys": [
                        {
                            "columns": ["[Request_ID]"],
                            "detailed_columns": [{"column": "[Request_ID]", "order": "ASC"}],
                            "constraint_name": "[PK_TO_Requests_Request_ID]",
                        }
                    ]
                },
                "index": [],
                "on": "[PRIMARY]",
                "partitioned_by": [],
                "primary_key": ["[Request_ID]"],
                "schema": "[dbo]",
                "table_name": "[TO_Requests]",
                "tablespace": None,
                "with": {
                    "on": None,
                    "properties": [
                        {"name": "PAD_INDEX", "value": "OFF"},
                        {"name": "STATISTICS_NORECOMPUTE", "value": "OFF"},
                        {"name": "IGNORE_DUP_KEY", "value": "OFF"},
                        {"name": "ALLOW_ROW_LOCKS", "value": "ON"},
                        {"name": "ALLOW_PAGE_LOCKS", "value": "ON"},
                    ],
                },
            },
            {
                "alter": {},
                "checks": [],
                "clustered_primary_key": [{"column": "[ID]", "order": "ASC"}],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "[ID]",
                        "nullable": False,
                        "references": None,
                        "size": (1, 1),
                        "type": "[int] IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[ProfileID]",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "[int]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[Title]",
                        "nullable": True,
                        "references": None,
                        "size": 50,
                        "type": "[varchar]",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "primary_keys": [
                        {"columns": ["[ID]"],
                         "detailed_columns": [{"column": "[ID]", "order": "ASC"}],
                         "constraint_name": "[PK_ToDo_ID]"}
                    ]
                },
                "index": [],
                "on": "[PRIMARY]",
                "partitioned_by": [],
                "primary_key": ["[ID]"],
                "schema": "[dbo]",
                "table_name": "[ToDo]",
                "tablespace": None,
                "textimage_on": "[PRIMARY]",
                "with": {
                    "on": None,
                    "properties": [
                        {"name": "PAD_INDEX", "value": "OFF"},
                        {"name": "STATISTICS_NORECOMPUTE", "value": "OFF"},
                        {"name": "IGNORE_DUP_KEY", "value": "OFF"},
                        {"name": "ALLOW_ROW_LOCKS", "value": "ON"},
                        {"name": "ALLOW_PAGE_LOCKS", "value": "ON"},
                    ],
                },
            },
            {
                "alter": {},
                "checks": [],
                "clustered_primary_key": [
                    {"column": "[ToDoCommentsId]", "order": "ASC"}
                ],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "[ToDoCommentsId]",
                        "nullable": False,
                        "references": None,
                        "size": (1, 1),
                        "type": "[int] IDENTITY",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[CreatedBy]",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "[int]",
                        "unique": False,
                    },
                ],
                "constraints": {
                    "primary_keys": [
                        {
                            "columns": ["[ToDoCommentsId]"],
                            "detailed_columns": [{"column": "[ToDoCommentsId]", "order": "ASC"}],
                            "constraint_name": "[PK_ToDoComments_ToDoCommentsId]",
                        }
                    ]
                },
                "index": [],
                "on": "[PRIMARY]",
                "partitioned_by": [],
                "primary_key": ["[ToDoCommentsId]"],
                "schema": "[dbo]",
                "table_name": "[ToDoComments]",
                "tablespace": None,
                "textimage_on": "[PRIMARY]",
                "with": {
                    "on": None,
                    "properties": [
                        {"name": "PAD_INDEX", "value": "OFF"},
                        {"name": "STATISTICS_NORECOMPUTE", "value": "OFF"},
                        {"name": "IGNORE_DUP_KEY", "value": "OFF"},
                        {"name": "ALLOW_ROW_LOCKS", "value": "ON"},
                        {"name": "ALLOW_PAGE_LOCKS", "value": "ON"},
                    ],
                },
            },
        ],
        "types": [],
    }

    assert expected == result


def test_next_value_for():

    ddl = """CREATE TABLE [dbo].[SLIPEVENTO] (
    [cdSLIP] [bigint] NOT NULL
    DEFAULT NEXT VALUE FOR [dbo].[sqCdSLIPEvt] )"""
    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        "ddl_properties": [],
        "domains": [],
        "schemas": [],
        "sequences": [],
        "tables": [
            {
                "alter": {},
                "checks": [],
                "columns": [
                    {
                        "check": None,
                        "default": {"next_value_for": "[dbo].[sqCdSLIPEvt]"},
                        "name": "[cdSLIP]",
                        "nullable": False,
                        "references": None,
                        "size": None,
                        "type": "[bigint]",
                        "unique": False,
                    }
                ],
                "index": [],
                "partitioned_by": [],
                "primary_key": [],
                "schema": "[dbo]",
                "table_name": "[SLIPEVENTO]",
                "tablespace": None,
            }
        ],
        "types": [],
    }
    assert expected == result


def test_primary_key_clustered():
    ddl = """
    USE [sasgolddevdb]
    GO
    /****** Object:  Table [aud].[tcal_tgt]    Script Date: 11/11/2021 11:18:41 AM ******/
    SET ANSI_NULLS ON
    GO
    SET QUOTED_IDENTIFIER ON
    GO
    CREATE TABLE [aud].[tcal_tgt](
        [TCAL_SID] [decimal](30, 0) NOT NULL,
        [TERM_YR] [varchar](4) NULL,
        [REC_DELETED_BY] [varchar](25) NULL,
        [SYSTEM_OPERATION] [varchar](1) NULL,
    PRIMARY KEY CLUSTERED
    (
        [TCAL_SID] ASC, [TERM_YR] DESC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF,
    IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 80) ON [PRIMARY]
    ) ON [PRIMARY]
    GO"""
    result = DDLParser(ddl).run(group_by_type=True)
    expected = {
        "comments": [
            "***** Object:  Table [aud].[tcal_tgt]    Script Date: "
            "11/11/2021 11:18:41 AM ******/"
        ],
        "ddl_properties": [
            {"name": "ANSI_NULLS", "value": "ON"},
            {"name": "QUOTED_IDENTIFIER", "value": "ON"},
        ],
        "domains": [],
        "schemas": [],
        "sequences": [],
        "tables": [
            {
                "alter": {},
                "checks": [],
                "columns": [
                    {
                        "check": None,
                        "default": None,
                        "name": "[TCAL_SID]",
                        "nullable": False,
                        "references": None,
                        "size": (30, 0),
                        "type": "[decimal]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[TERM_YR]",
                        "nullable": False,
                        "references": None,
                        "size": 4,
                        "type": "[varchar]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[REC_DELETED_BY]",
                        "nullable": True,
                        "references": None,
                        "size": 25,
                        "type": "[varchar]",
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "name": "[SYSTEM_OPERATION]",
                        "nullable": True,
                        "references": None,
                        "size": 1,
                        "type": "[varchar]",
                        "unique": False,
                    },
                ],
                "index": [],
                "on": "[PRIMARY]",
                "partitioned_by": [],
                "primary_key": ["[TCAL_SID]", "[TERM_YR]"],
                "schema": "[aud]",
                "table_name": "[tcal_tgt]",
                "tablespace": None,
                "clustered_primary_key": [
                    {"column": "[TCAL_SID]", "order": "ASC"},
                    {"column": "[TERM_YR]", "order": "DESC"},
                ],
                "with": {
                    "on": None,
                    "properties": [
                        {"name": "PAD_INDEX", "value": "OFF"},
                        {"name": "STATISTICS_NORECOMPUTE", "value": "OFF"},
                        {"name": "IGNORE_DUP_KEY", "value": "OFF"},
                        {"name": "ALLOW_ROW_LOCKS", "value": "ON"},
                        {"name": "ALLOW_PAGE_LOCKS", "value": "ON"},
                        {"name": "FILLFACTOR", "value": "80"},
                    ],
                },
            }
        ],
        "types": [],
    }
    assert expected == result
