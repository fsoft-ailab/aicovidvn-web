import psycopg2
from utils import log_service
from instance import environment

connection = None

class PostgresDB():
    cursor = None
    handler_status = None

    def _handler_status(self, msg):
        if self.handler_status is not None:
            self.handler_status(msg, 2000)

    def __init__(self, user=environment.DB_USER,
                 password=environment.DB_PASSWORD,
                 host=environment.DB_HOST,
                 port=environment.DB_PORT,
                 database=environment.DB_NAME, handler_status=None):
        self.handler_status = handler_status

        log_service.info(
            "Connect to database : host = {} | port = {} | database name = {} | user = {}".format(host, port, database,
                                                                                                  user))
        try:
            global connection
            if connection is None:
                connection = psycopg2.connect(user=user,
                                                   password=password,
                                                   host=host,
                                                   port=port,
                                                   database=database)
            # Print PostgreSQL version
            record = self.execute_query("SELECT version();").fetchone()
            log_service.info("You are connected to: {}".format(record))
            self._handler_status("You are connected to: {}".format(record))
        except (Exception, psycopg2.Error) as error:
            self._handler_status("Connect to database fail")
            log_service.error(str(error))

    def get_all_public_table(self):
        self._handler_status("Get all public table")
        return self.execute_query(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public';").fetchall()

    def get_table_column(self, table_name):
        self._handler_status("Get all table column")
        return self.execute_query(
            "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{}';".format(
                table_name)).fetchall()

    def execute_query_with_data(self, query, data=None):
        global connection
        log_service.debug("Query: {}".format(query))
        self.cursor = connection.cursor()
        if data is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)

        connection.commit()

        log_service.debug("{} row effect".format(self.cursor.rowcount))
        self._handler_status("Query: {} | Row effects = {}".format(query, self.cursor.rowcount))
        return self.cursor

    def execute_query(self, query, data=None):
        log_service.debug("Query: {}".format(query))
        self.cursor = connection.cursor()
        if data is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)
        return self.cursor

    def close_connection(self):
        self.cursor.close()
