#!/usr/bin/env bash

set -e

TIMEOUT=${WAIT_FOR_STARTUP:-300}
RCON_ADDRESS=${RCON_ADDRESS:-127.0.0.1}
RCON_PORT=${RCON_PORT:-25575}
python /usr/local/bin/wait_for_tcp.py $RCON_ADDRESS $RCON_PORT $TIMEOUT

python app.py

