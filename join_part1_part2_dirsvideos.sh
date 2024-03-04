#!/usr/bin/env bash

cd /home/ubuntu/zipped_dataset

for f in *; do
    if [ -d ${f} ]; then
        # Will not run if no directories are available
        echo "working on "$f
        cd $f
        mkdir videos
        mv video_part1/*.mpg videos/
        mv video_part2/*.mpg videos/
		rm -rf video_part1 video_part2
        cd ..
    fi
done
