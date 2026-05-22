#!/usr/bin/env bash

stdbuf -oL swaymsg -t get_tree | jq -r '.. | select(.focused?) | .name' \
    && swaymsg -m -t subscribe '["window"]' |
jq --unbuffered -rc '
select(.container.name != null)
| .container.name
'
