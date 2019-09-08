#!/bin/bash
docker run \
--name magic-cards \
--restart=always \
-d \
-p 5000:5000 \
-v /home/pi/kv-guessgame/magic-cards/config:/usr/src/app/config \
--device=/dev/input/event0 \
jonmaddox/magic-cards
