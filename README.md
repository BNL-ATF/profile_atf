# profile_atf
ATF IPython startup files for data collection via sockets

## Used Environment Variables

| Variable               | Requirement     | Description                      |
| ---------------------- | ------------- | -------------------------------- |
| `ATF_SOCKET_HOST`       | Required      | Socket Host (e.g. "localhost")        |
| `ATF_SOCKET_PORT`        | Required      | Socket Port number (int, > 1024)         |
| `PYLON_ROOT`             | Required      | e.g. "/opt/pylon5"                     |
| `ATF_OPEN_CONN_ONCE`     | Optional      | Open connection on every call, default is "no", to enable "yes"  |
| `ATF_SIREPO_URL`         | Optional      | Sirepo server URL with port number e.g. http://localhost:8000   |
| `PYLON_CAMEMU`           | Optional      | Number of Emulated Cameras (int)          |
| `PYLON_CAM_PIXEL_FORMAT` | Optional      | Default "Mono12", to change e.g. "Mono16"     |

## Start command example

```bash
ATF_OPEN_CONN_ONCE=yes ATF_SOCKET_HOST="localhost" ATF_SOCKET_PORT=5000 ATF_SIREPO_URL="http://localhost:8000" PYLON_CAMEMU=10 PYLON_CAM_PIXEL_FORMAT="Mono16" ipython --profile-dir=.
```
