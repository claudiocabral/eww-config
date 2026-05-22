network=$(iwctl station wlan0 show)
name=$(awk -F'Connected network[[:space:]]+' '/Connected network/ {print $2}' <<< $network)
signal=$(awk -F'AverageRSSI[[:space:]]+' '/AverageRSSI/ {print $2}' <<< $network)

echo "   " $name $signal
