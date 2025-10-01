#!/bin/sh

base_dir=$(pwd)

input_folder="$base_dir/assets/videos"
output_folder="$base_dir/assets/streams"

mkdir -p "$output_folder"

for file in "$input_folder"/*; do
    case "$file" in
        *.mp4|*.MOV)
            file_name=$(basename "$file")
            file_name="${file_name%.*}"
            output_path="$output_folder/$file_name"

            if [ -d "$output_path" ]; then
                echo "Skipping: Folder '$output_path' exists. Do not process file: '$file'."
                continue
            fi

            mkdir -p "$output_path"

            ffmpeg -i "$file" \
                -map 0:v:0 -map 0:a:0 \
                -s:v:0 360x640 -c:v:0 libx264 -b:v:0 800k -maxrate:v:0 850k -bufsize:v:0 1200k \
                -map 0:v:0 -map 0:a:0 \
                -s:v:1 480x854 -c:v:1 libx264 -b:v:1 1200k -maxrate:v:1 1280k -bufsize:v:1 1600k \
                -map 0:v:0 -map 0:a:0 \
                -s:v:2 720x1280 -c:v:2 libx264 -b:v:2 2800k -maxrate:v:2 2996k -bufsize:v:2 4200k \
                -map 0:v:0 -map 0:a:0 \
                -s:v:3 1080x1920 -c:v:3 libx264 -b:v:3 5000k -maxrate:v:3 5500k -bufsize:v:3 7500k \
                -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2 v:3,a:3" \
                -f hls \
                -hls_time 30 \
                -hls_playlist_type vod \
                -hls_segment_filename "$output_path/output_%v_%03d.ts" \
                -master_pl_name master.m3u8 \
                "$output_path/output_%v.m3u8"

            echo "[FFmpeg] Completed: $file"
            ;;
        *) 
            echo "Skipping unsupported file: $file"
            ;;
    esac
done

echo "[FFmpeg] All conversions complete!"
