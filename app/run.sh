#!/usr/bin/env bash

function start () {
    source .demo_api/bin/activate
    cd app && gunicorn -b 0.0.0.0:5000 app
}

function stop () {
    ps -ef | grep gunicorn | awk '{print $2}' | xargs kill -9
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    *)
    echo "Usage: run.sh {start|stop}"
    exit 1
esac