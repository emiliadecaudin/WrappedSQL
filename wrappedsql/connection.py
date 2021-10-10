#----Standard Library Imports------------------------------------------------#

from typing import Text, TYPE_CHECKING

#----Pip Library Imports-----------------------------------------------------#

import pymysql

#----Internal Imports--------------------------------------------------------#

if TYPE_CHECKING:
    from .database import WrappedDatabase
from .cursor import WrappedCursor

#----Class Declarations------------------------------------------------------#

class WrappedConnection:

    """This class wraps around pymysql Connections."""

    #----Instance Methods----------------------------------------------------#

    def __init__(self, wrapped_database: 'WrappedDatabase', database, **options) -> None:

        self.wrapped_database = wrapped_database
        self.in_use = False
        self.database = database
        self.options = options

        self.connection = pymysql.connect(host = wrapped_database.host, port = wrapped_database.port, user = wrapped_database.user, password = wrapped_database.password, ssl = wrapped_database.ssl, database = database, **options)
        self.connection.close

    def __str__(self) -> Text:

        return(f"{self.wrapped_database}/{self.database}{'?' + self.options.__str__() if self.options else ''}")

    def cursor(self, buffered: bool = False, dict: bool = False) -> WrappedCursor:

        return WrappedCursor(self, buffered, dict)

    def close(self) -> None:

        self.connection.close()