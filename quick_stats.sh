#!/bin/bash

CSV_FILE="/Users/luke/cursor-projs/screenshot-job/log.csv"

if [ ! -f "$CSV_FILE" ]; then
    echo "Error: CSV file not found at $CSV_FILE"
    exit 1
fi

# Get today's date in the format used in the CSV
TODAY=$(date +"%Y-%m-%d")

# Count applications for today
TODAY_COUNT=$(grep "$TODAY" "$CSV_FILE" | wc -l)

# Count total applications
TOTAL_COUNT=$(tail -n +2 "$CSV_FILE" | wc -l)

# Get the date of the first application
FIRST_DATE=$(tail -n +2 "$CSV_FILE" | cut -d',' -f5 | sort | head -n 1 | cut -d' ' -f1)

# Calculate average applications per day
if [ -n "$FIRST_DATE" ]; then
    DAYS_SINCE_START=$(( ($(date +%s) - $(date -j -f "%Y-%m-%d" "$FIRST_DATE" +%s)) / 86400 ))
    if [ $DAYS_SINCE_START -gt 0 ]; then
        AVG_PER_DAY=$(echo "scale=2; $TOTAL_COUNT / $DAYS_SINCE_START" | bc)
    else
        AVG_PER_DAY=$TOTAL_COUNT
    fi
else
    DAYS_SINCE_START=0
    AVG_PER_DAY=0
fi

# Get the last 5 companies applied to
LAST_5_COMPANIES=$(tail -n 5 "$CSV_FILE" | cut -d',' -f2 | tail -r)

echo "Quick Job Application Stats:"
echo "----------------------------"
echo "Applications today: $TODAY_COUNT"
echo "Total applications: $TOTAL_COUNT"
echo "Average applications per day: $AVG_PER_DAY"
echo "Days since first application: $DAYS_SINCE_START"
echo ""
echo "Last 5 companies applied to:"
echo "$LAST_5_COMPANIES"
echo ""
echo "Remaining applications for today's goal (30): $((30 - TODAY_COUNT))"
