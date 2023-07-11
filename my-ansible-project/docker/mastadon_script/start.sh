#!/bin/bash

# Prompt for arguments
read -p "Enter Database Name: " arg1
read -p "Enter IP address: " arg2
read -p "Enter Desired Time (in 24-hour format, e.g., 09:00): " desired_time_input

# Extract hour and minute from the desired time input
desired_hour=${desired_time_input:0:2}
desired_minute=${desired_time_input:3:2}

# Validate the desired time input
if ! [[ "$desired_hour" =~ ^[0-9]+$ ]] || ! [[ "$desired_minute" =~ ^[0-9]+$ ]] || (( desired_hour < 0 || desired_hour > 23 )) || (( desired_minute < 0 || desired_minute > 59 )); then
    echo "Invalid desired time input. Please enter a valid time in the format HH:MM (24-hour format)."
    exit 1
fi

# Define the job name
job_name="my_cron_job"

# Format the cron job entry with job name, argument, and desired time
cron_entry="$desired_minute $desired_hour * * * /bin/bash /root/mastadon_script/new_harvester.sh \"$arg1\" \"$arg2\" >> /root/cron.log 2>&1 # $job_name-$arg1"

# Format the cron job entry with job name, argument, and desired time for old_harvester.sh
cron_entry2="$desired_minute $desired_hour * * * /bin/bash /root/mastadon_script/old_harvester.sh \"$arg1\" \"$arg2\" >> /root/cron.log 2>&1 # $job_name-$arg1"

# Create a temporary file to hold the cron job entry
cron_temp=$(mktemp)
echo "$cron_entry" > "$cron_temp"
echo "$cron_entry2" >> "$cron_temp"

# Add the cron job by importing the temporary file
crontab "$cron_temp"

# Start the cron service in the background
service cron start

# Keep the container running indefinitely
tail -f /dev/null
