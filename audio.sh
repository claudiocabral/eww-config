#!/bin/bash

MODE="${1:-all}"

get_audio_info() {
    VOLUME_INFO=$(wpctl get-volume @DEFAULT_SINK@)
    VOLUME=$(echo "$VOLUME_INFO" | awk '{print int($2 * 100)}')

    MUTED=false
    if echo "$VOLUME_INFO" | grep -qi "\[muted\]"; then
        MUTED=true
    fi

    HEADPHONE=false
    if command -v pactl &>/dev/null; then
        DEFAULT_SINK=$(pactl get-default-sink 2>/dev/null)
        if [ -n "$DEFAULT_SINK" ]; then
            ACTIVE_PORT=$(pactl list sinks 2>/dev/null | grep -A 40 "^[[:space:]]*Name:[[:space:]]*${DEFAULT_SINK}$" | grep "Active Port:" | awk '{print $NF}')
            if echo "$ACTIVE_PORT" | grep -qi "headphone"; then
                HEADPHONE=true
            fi
        fi
    fi

    if [ "$MUTED" = true ]; then
        ICON=""
    elif [ "$HEADPHONE" = true ]; then
        ICON=""
    else
        ICON=""
    fi

    case "$MODE" in
        volume) echo "{\"volume\": $VOLUME}" ;;
        icon)   echo "$ICON" ;;
        all)    echo "{\"volume\": $VOLUME, \"icon\": \"$ICON\"}" ;;
    esac
}

get_audio_info

pactl subscribe 2>/dev/null | while read -r event; do
    case "$event" in
        *"'change' on sink"*|*"'change' on server"*)
            get_audio_info
            ;;
    esac
done
