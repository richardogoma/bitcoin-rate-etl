#!/usr/bin/env bash
set -e

# Make processed data directory
mkdir -p data/processed

# ------------------------------------------------------------------------
# Check if the ETL pipeline process is already running
if pgrep -f etl_pipeline.py >/dev/null; then
    # Grab the PID of the ETL pipeline process
    pid=$(pgrep -f etl_pipeline.py)
    echo -e "ETL pipeline is already running. Skipping the startup command. \nYou can kill the process by executing: kill $pid"
else
    # -----------------------------------------------------------------------
    # Calculate the delay until the start of the next minute
    current_seconds=$(date +%s)
    next_minute_seconds=$(( (current_seconds / 60 + 1) * 60 ))
    delay_seconds=$((next_minute_seconds - current_seconds))

    # Get the current timestamp
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")

    # Echo the sleep duration, timestamp, and reason to console
    echo "[$timestamp] Sleeping for $delay_seconds seconds before starting the ETL pipeline to sync with the data source refresh schedule."

    # Define the characters for the rolling cursor animation
    cursor_chars=("◐" "◓" "◑" "◒")

    # Calculate the duration for each frame
    frame_duration=$((delay_seconds / ${#cursor_chars[@]}))

    # Sleep until the start of the next minute
    for ((i = 0; i < delay_seconds; i++)); do
        # Calculate the index of the current cursor character
        animation_index=$((i / frame_duration % ${#cursor_chars[@]}))

        # Print the current cursor character and timestamp
        timestamp=$(date +"%Y-%m-%d %H:%M:%S")
        echo -ne "[$timestamp] ${cursor_chars[animation_index]}\r"

        # Sleep for 1 second
        sleep 1
    done

    # Start the ETL pipeline in the background and append stdout to output.log
    nohup nice -n 10 python3 -u etl_pipeline.py >> output.log 2>&1 &

    # Echo message before the sleep command
    echo "Waiting for a few seconds to allow the process to start..."

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
fi
