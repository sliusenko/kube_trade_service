EXAMPLE:
Створити ревізію:
alembic -c alembic_trade.ini revision -m "add symbol_id to exchange_symbols"
Відредагувати файл у versions/.
Виконати міграцію:
alembic -c alembic_trade.ini upgrade head
Перевірити у psql:
\d exchange_symbols;
