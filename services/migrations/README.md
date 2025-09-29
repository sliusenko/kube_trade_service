EXAMPLE:
Створити ревізію:
alembic -c alembic_trade.ini revision -m "add symbol_id to exchange_symbols"
Відредагувати файл у versions/.
Виконати міграцію:
alembic -c alembic_trade.ini upgrade head
Перевірити у psql:
\d exchange_symbols;


alembic revision --autogenerate -m "..."
alembic upgrade head


alembic revision --autogenerate -m "init full schema"
alembic upgrade head
