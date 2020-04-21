#! /bin/sh
for i in *; do ffmpeg -i $i -vf scale=640:360 down/$i; done