#!/usr/bin/env bash
set -e

# Run "make all" command to set up dependencies and other tasks
make all

# Start the ETL pipeline in the background with nohup
nohup nice -n 10 python3 -u etl_pipeline.py > output.log 2>&1 &

# Sleep for a few seconds to allow the process to start
sleep 5

# Grab the PID of the ETL pipeline process
pid=$(pgrep -f etl_pipeline.py)

# Check if the process is running
if [ -n "$pid" ]; then
    echo -e "ETL pipeline is running. PID: $pid \nYou can kill the process by executing: kill $pid"

    # Monitor resource allocation using ps
    ps -p "$pid" -o user,pid,ppid,ni,time,state,start,%cpu,%mem
else
    echo "ETL pipeline failed to start."
fi
