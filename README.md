# profile_atf
ATF IPython startup files for data collection via sockets

Required Environment Variables

| 10-devices                                                               |
| ------------------------------------------------------------------------ |
| Variable              | Condition     | Description                      |
| --------------------- | ------------- | -------------------------------- |
| ATF_SOCKET_HOST       | Required      | Socket Host ("localhost")        |
| ATF_SOCKET_PORT       | Required      | Socket Port number (int)         |
| ATF_OPEN_CONN_ONCE    | Required      | Open connection ("yes")          |
| ------------------------------------------------------------------------ |
| 20-madx                                                                  |
| ------------------------------------------------------------------------ |
| ATF_SIREPO_URL        | Optional      | Sirepo connection (use Sirepo)   |
| ------------------------------------------------------------------------ |
| 30-basler                                                                |
| ------------------------------------------------------------------------ |
|PYLON_CAMEMU           | Optional      | Emulated Camera (int)            |
|PYLON_CAM_PIXEL_FORMAT |               |  ("Mono16")                      |

