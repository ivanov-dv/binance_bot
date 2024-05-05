import psycopg2

from config import *


def try_except_connect_db(func):
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            return data
        except Exception as _ex:
            logger.error(f"Ошибка БД. {func.__qualname__} {_ex}")

    return wrapper


class DB:
    """Класс для работы с БД"""

    def __init__(self, host, user, password, database, autocommit):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.connection.autocommit = autocommit

    @try_except_connect_db
    def start_and_create_tables(self) -> None:
        """Принт версии БД и создание таблиц"""

        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            logger.trace(cursor.fetchone())
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS monitoring_pairs
                (
                    id int,
                    name_bot text,
                    amount_pairs int,
                    master_iteration_count bigint,
                    slave_iteration_count bigint,
                    target_percent int,
                    time_update timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT monitoring_pairs_pkey PRIMARY KEY (id)
                );
                CREATE TABLE IF NOT EXISTS monitoring_open_orders
                (
                    id int,
                    name_bot text,
                    amount_open_positions int,
                    iterations_count int,
                    open_orders_info_json jsonb,
                    time_update timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT monitoring_open_orders_pkey PRIMARY KEY (id)
                );
                CREATE TABLE IF NOT EXISTS list_pairs
                (
                    id int,
                    list_pairs text[],
                    time_update timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT list_pairs_pkey PRIMARY KEY (id)
                );
            """)
            self.connection.commit()
            logger.trace("Таблицы в БД созданы")

    @try_except_connect_db
    def update_monitoring_pairs_data(self,
                                     name_bot,
                                     amount_pairs,
                                     master_iteration_count,
                                     slave_iteration_count,
                                     target_percent) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO monitoring_pairs
                (id, name_bot, amount_pairs, master_iteration_count, slave_iteration_count, target_percent)
                VALUES 
                (1, '{name_bot}', {amount_pairs}, {master_iteration_count}, {slave_iteration_count}, {target_percent})
                ON CONFLICT (id) DO UPDATE
                SET name_bot = '{name_bot}',
                amount_pairs = {amount_pairs}, 
                master_iteration_count = {master_iteration_count}, 
                slave_iteration_count = {slave_iteration_count}, 
                target_percent = {target_percent}, 
                time_update = CURRENT_TIMESTAMP;
            """)
            self.connection.commit()

    @try_except_connect_db
    def update_monitoring_open_orders_data(self,
                                           name_bot,
                                           amount_open_positions,
                                           iterations_count,
                                           open_orders_info_json) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(f"""
            
                INSERT INTO monitoring_open_orders
                (id, name_bot, amount_open_positions, iterations_count, open_orders_info_json)
                VALUES (1, '{name_bot}', {amount_open_positions}, {iterations_count}, '{open_orders_info_json}')
                ON CONFLICT (id) DO UPDATE
                SET name_bot = '{name_bot}',
                amount_open_positions = {amount_open_positions},
                iterations_count = {iterations_count},
                open_orders_info_json = '{open_orders_info_json}',
                time_update = CURRENT_TIMESTAMP;
            """)
            self.connection.commit()

    def update_list_pairs(self, list_pairs):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO list_pairs
                (id, list_pairs)
                VALUES (1, ARRAY{list_pairs})
                ON CONFLICT (id) DO UPDATE
                SET list_pairs = ARRAY{list_pairs},
                time_update = CURRENT_TIMESTAMP;
            """)
            self.connection.commit()

    def get_list_pairs(self):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT list_pairs FROM list_pairs WHERE id = 1;
            """)
            list_pairs = cursor.fetchone()[0]
            return list_pairs
