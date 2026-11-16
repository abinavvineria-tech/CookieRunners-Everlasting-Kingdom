#!/bin/bash
#===============================================================================
# CRUSMI Gateway Startup Script
# Cookie Runners United Shadow Milk India
# "We stand together, we play together, and we rise together."
#===============================================================================

#-------------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------------
# Configured / active profile (marked with ◆ in the profile list)
PROFILE_NAME="crusmi"

# Log directory and file for the gateway
LOG_DIR="$HOME/.hermes/profiles/cookiebloomnexus/logs"
LOG_FILE="$LOG_DIR/gateway.log"

#-------------------------------------------------------------------------------
# Ensure the log directory exists
#-------------------------------------------------------------------------------
mkdir -p "$LOG_DIR"

#-------------------------------------------------------------------------------
# Export the profile so hermes picks up the configured profile
#-------------------------------------------------------------------------------
export HERMES_PROFILE="$PROFILE_NAME"

#-------------------------------------------------------------------------------
# Start the hermes gateway in the background
#-------------------------------------------------------------------------------
echo "============================================================"
echo "  CRUSMI Gateway Startup"
echo "  Profile : $PROFILE_NAME"
echo "  Log file: $LOG_FILE"
echo "============================================================"

nohup hermes gateway run > "$LOG_FILE" 2>&1 &

GATEWAY_PID=$!

echo ""
echo "Gateway started in the background (PID: $GATEWAY_PID)"
echo "Profile   : $PROFILE_NAME"
echo "Logs      : $LOG_FILE"
echo ""
echo "To follow logs live:  tail -f $LOG_FILE"
echo "To stop the gateway:  kill $GATEWAY_PID"
