#!/bin/bash

get_volume() {
    wpctl get-volume @DEFAULT_SINK@ | awk '{print int($2 * 100)}'
}

get_volume

pactl subscribe | while read -r event; do
    case "$event" in
        *"'change' on sink"*)
            get_volume
            ;;
    esac
done
