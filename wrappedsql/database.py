#----Standard Library Imports------------------------------------------------#

from typing import Text

#----Internal Imports--------------------------------------------------------#

from .connection import WrappedConnection

#----Class Declarations------------------------------------------------------#

class WrappedDatabase:

    #----Instance Methods----------------------------------------------------#

    def __init__(self, host: Text, user: Text, port: int = 3306, password: Text = None, ssl: dict = None) -> None:

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ssl = ssl

        self.connections = []

    def __str__(self) -> Text:

        return(f"mysql://{self.user}@{self.host}:{self.port}")

    def __enter__(self) -> 'WrappedDatabase':

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:

        self.closeAll()

    def getConnection(self, database: Text, **options) -> WrappedConnection:

        if (self.connections):

            for connection in self.connections:

                if(not connection.in_use and connection.database == database and connection.options == options):

                    return connection

        connection = WrappedConnection(self, database = database, **options)
        self.connections.append(connection)

        return connection

    def closeAll(self) -> None:

        for connection in self.connections:

            connection.close()