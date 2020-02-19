#!/bin/bash

WORK_DIR=/home/worker/services/closewindow
cd ${WORK_DIR}

#pid=`cat ${WORK_DIR}/var/cw.pid`

#if [ ! -e /proc/$pid -a /proc/$pid/exe ]; then
#    echo 'program is not running'
#else
#    echo 'program is already running'
#    kill -9 ${pid}
#fi
#nohup python3 ${WORK_DIR}/main.py >${WORK_DIR}/logs/start.log 2>&1 &
#echo $! > ${WORK_DIR}/var/cw.pid

/usr/bin/python3 ${WORK_DIR}/main.py >${WORK_DIR}/logs/start.log