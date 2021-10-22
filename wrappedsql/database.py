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

        return(f"mysql://{self.user}@{self.host}:{self.port}")

    def __enter__(self) -> 'WrappedDatabase':

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:

        self.closeAll()

    def getConnection(self, database: str, **options):

        connection = self.generator.connect(host = self.host,
                                     port = self.port,
                                     user = self.user,
                                     password = self.password,
                                     ssl = self.ssl,
                                     database = database,
                                     **options)

        self.connections.append(connection)

        return connection

    def closeAll(self) -> None:

        for connection in [connection for connection in self.connections if connection.open]:

            connection.close()