print(f"Loading {__file__}")

import atexit

from atfdb import atfdb


def teardown_socket_connection(func, atfdb):
    if func():
        print("Closing socket connection to atf_db...")
        atfdb.host_disconnect()
    else:
        print(
            "Socket connection to atf_db is managed per call.\n"
            "If you wish to open/close connection once per session "
            "set the environment variable ATF_OPEN_CONN_ONCE to 'yes'."
        )


atexit.register(teardown_socket_connection, check_conn_once, atfdb)
