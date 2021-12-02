#----Class Declarations------------------------------------------------------#

class WrappedDatabase:

    #----Instance Methods----------------------------------------------------#

    def __init__(self, generator: type, /, host: str, user: str, port: int = 3306, password: str = None, ssl: dict = None) -> None:

        self.generator = generator
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ssl = ssl

        self.connections = []

    def __str__(self) -> str:

        return(f"mysql{'ssl' if self.ssl else ''}://{self.user}@{self.host}:{self.port}")

    def __enter__(self) -> 'WrappedDatabase':

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:

        self.closeAll()

    def getConnection(self, database: str, **options) -> 'pymysql.connections.Connection | ...':

        connection = self.generator.connect(host = self.host,
                                     port = self.port,
                                     user = self.user,
                                     password = self.password,
                                     ssl = self.ssl,
                                     database = database,
                                     **options)

        self.connections.append(connection)

        return connection

    def cursorGenerator(self, buffered: bool, dictionary: bool) -> type:

        match self.generator:
            case pymysql:
                match (buffered, dictionary):
                    case (False, False):
                        return pymysql.cursors.SSCursor
                    case (False, True):
                        return pymysql.cursors.SSDictCursor
                    case (True, False):
                        return pymysql.cursors.Cursor
                    case (True, True):
                        return pymysql.cursors.DictCursor

    def closeAll(self) -> None:

        for connection in [connection for connection in self.connections if connection.open]:

            connection.close()