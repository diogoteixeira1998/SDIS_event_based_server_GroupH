
> sqlite3

# para sair 
> .quit

# criar DB
no diretorio onde queres a .db
> sqlite [DB_name].db

# exemplo

  > CREATE TABLE names (
  >   ...> ID INT PRIMARY KEY NOT NULL,
  >   ...> NAME TEXT NOT NULL
  >   ...> );

> .schema names # estrutura da tabela

> .tables  # tabelas criadas


# importar csv

> .mode csv

> .import file_name.csv table_name


