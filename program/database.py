import psycopg2


class DatabaseManager:
    def __init__(self, db_name: str, params: dict):
        self.db_name = db_name
        self.params = params
        self.connection = None

    def connect(self, db_name):
        if db_name is None:
            db_name = self.db_name
        self.connection = psycopg2.connect(dbname=db_name, **self.params)
        self.connection.autocommit = True

    def close_connect(self):
        if self.connection:
            self.connection.close()

    def create_database(self):
        self.connect(db_name='postgres')
        with self.connection.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
            cur.execute(f"CREATE DATABASE {self.db_name}")
        print(f"База данных '{self.db_name}' успешно создана.")
        self.close_connect()

    def create_table(self):
        self.connect(db_name=self.db_name)
        with self.connection.cursor() as cur:
            cur.execute('''
                    CREATE TABLE IF NOT EXISTS company (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(200),
                        ogrn VARCHAR(20) NOT NULL, 
                        inn VARCHAR(20) NOT NULL, 
                        date DATE
                    )
                    ''')

            cur.execute('''
            CREATE TABLE IF NOT EXISTS phone (
            id SERIAL PRIMARY KEY,
            company_id INT REFERENCES company(id),
            phone VARCHAR(20)
            )
            ''')
        self.connection.commit()
        self.close_connect()
