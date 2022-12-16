print(f"Loading {__file__}")

import atexit


def teardown_my_shell(func, atf_db):
    if func():
        print("Closing socket connection to atf_db...")
        atf_db.host_disconnect()
    else:
        print(
            "Socket connection to atf_db is managed per call.\n"
            "If you wish to open/close connection once per session "
            "set the environment variable ATF_OPEN_CONN_ONCE to 'yes'."
        )


atexit.register(teardown_my_shell, check_conn_once, atf_db)
