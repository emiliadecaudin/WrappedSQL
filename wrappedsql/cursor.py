#----Standard Library Imports------------------------------------------------#

from typing import Any, Iterable, Iterator, Text, Tuple, TYPE_CHECKING

#----Pip Library Imports-----------------------------------------------------#

import pymysql.cursors

#----Internal Imports--------------------------------------------------------#

if TYPE_CHECKING:
    from .connection import WrappedConnection

#----Class Declarations------------------------------------------------------#

class WrappedCursor:

    """This class wraps around pymysql Cursors."""

    #----Instance Methods----------------------------------------------------#

    def __init__(self, wrapped_connection: 'WrappedConnection', buffered: bool = False, dict: bool = False) -> None:

        self.wrapped_connection = wrapped_connection

        if (buffered):

            if (dict):

                cursor_class = pymysql.cursors.SSDictCursor

            elif (not dict):

                cursor_class = pymysql.cursors.SSCursor

        elif (not buffered):

            if (dict):

                cursor_class = pymysql.cursors.DictCursor

            elif (not dict):

                cursor_class = pymysql.cursors.Cursor

        self.cursor = self.wrapped_connection.connection.cursor(cursor_class)

    def __iter__(self) -> Iterator[Tuple] | Iterator[dict[Text, Any]]:

        return self.cursor.__iter__()

    def execute(self, query: Text, args: Iterable = None) -> int:

        return self.cursor.execute(query, args)

    def executemany(self, query: Text, args: Iterable = None) -> int | None:

        return self.cursor.executemany(query, args)

    def fetchone(self) -> Tuple[Any, ...] | dict[Text, Any] | None:

        return self.cursor.fetchone()

    def fetchmany(self, size: int | None = None) -> Tuple[Tuple[Any, ...], ...] | Tuple[dict[Text, Any], ...]:

        return self.cursor.fetchmany(size)

    def fetchall(self) -> Tuple[Tuple[Any, ...], ...] | Tuple[dict[Text, Any], ...] | list[Tuple[Any, ...]]:

        return self.cursor.fetchall()

    def close(self) -> None:

        self.cursor.close()