import os
import subprocess

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
input_folder = os.path.join(base_dir, "asset/video")
output_folder = os.path.join(base_dir, "asset/stream")

os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):
    if not (file.endswith(".MOV") or file.endswith(".mp4")):
        continue

    input_file_path = os.path.join(input_folder, file)
    file_name, _ = os.path.splitext(file)
    output_path = os.path.join(output_folder, file_name)

    if os.path.exists(output_path):
        print(f"Skipping: Folder '{output_path}' exists. Do not process file: '{file}'.")
        continue

    os.makedirs(output_path)

    command = [
        "ffmpeg",
        "-i", input_file_path,
        "-map", "0:v:0", "-map", "0:a:0",
        "-s:v:0", "360x640", "-c:v:0", "libx264", "-b:v:0", "800k", "-maxrate:v:0", "850k", "-bufsize:v:0", "1200k",
        "-map", "0:v:0", "-map", "0:a:0",
        "-s:v:1", "480x854", "-c:v:1", "libx264", "-b:v:1", "1200k", "-maxrate:v:1", "1280k", "-bufsize:v:1", "1600k",
        "-map", "0:v:0", "-map", "0:a:0",
        "-s:v:2", "720x1280", "-c:v:2", "libx264", "-b:v:2", "2800k", "-maxrate:v:2", "2996k", "-bufsize:v:2", "4200k",
        "-map", "0:v:0", "-map", "0:a:0",
        "-s:v:3", "1080x1920", "-c:v:3", "libx264", "-b:v:3", "5000k", "-maxrate:v:3", "5500k", "-bufsize:v:3", "7500k",
        "-var_stream_map", "v:0,a:0 v:1,a:1 v:2,a:2 v:3,a:3",
        "-f", "hls",
        "-hls_time", "30",
        "-hls_playlist_type", "vod",
        "-hls_segment_filename", os.path.join(output_path, "output_%v_%03d.ts"),
        "-master_pl_name", "master.m3u8",
        os.path.join(output_path, "output_%v.m3u8")
    ]

    print(f"[FFmpeg] Processing: {file}")
    subprocess.run(command, check=True)
    print(f"[FFmpeg] Completed: {file}")

print("[FFmped] The conversion process is all complete !")
