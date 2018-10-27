#!/usr/bin/env bash
#   Use this script to test if a given TCP host/port are available

#!/bin/bash
# wait-for-it.sh

set -e

host="$1"
shift
cmd="$@"

sleep 45
exec "$@"