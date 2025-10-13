import Foundation

let fileManager = FileManager.default

let baseDir = fileManager.currentDirectoryPath
let inputFolder = "\(baseDir)/asset/video"
let outputFolder = "\(baseDir)/asset/stream"

try? fileManager.createDirectory(atPath: outputFolder, withIntermediateDirectories: true)

guard let files = try? fileManager.contentsOfDirectory(atPath: inputFolder) else {
    print("Input folder not found!")
    exit(1)
}

for file in files {
    if !(file.hasSuffix(".mp4") || file.hasSuffix(".MOV")) { continue }

    let inputFilePath = "\(inputFolder)/\(file)"
    let fileName = (file as NSString).deletingPathExtension
    let outputPath = "\(outputFolder)/\(fileName)"

    if fileManager.fileExists(atPath: outputPath) {
        print("Skipping: Folder '\(outputPath)' exists. Do not process file: '\(file)'.")
        continue
    }

    try? fileManager.createDirectory(atPath: outputPath, withIntermediateDirectories: true)

    let command = """
    ffmpeg -i "\(inputFilePath)" \
    -map 0:v:0 -map 0:a:0 -s:v:0 360x640 -c:v:0 libx264 -b:v:0 800k -maxrate:v:0 850k -bufsize:v:0 1200k \
    -map 0:v:0 -map 0:a:0 -s:v:1 480x854 -c:v:1 libx264 -b:v:1 1200k -maxrate:v:1 1280k -bufsize:v:1 1600k \
    -map 0:v:0 -map 0:a:0 -s:v:2 720x1280 -c:v:2 libx264 -b:v:2 2800k -maxrate:v:2 2996k -bufsize:v:2 4200k \
    -map 0:v:0 -map 0:a:0 -s:v:3 1080x1920 -c:v:3 libx264 -b:v:3 5000k -maxrate:v:3 5500k -bufsize:v:3 7500k \
    -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2 v:3,a:3" \
    -f hls -hls_time 30 -hls_playlist_type vod \
    -hls_segment_filename "\(outputPath)/output_%v_%03d.ts" \
    -master_pl_name master.m3u8 "\(outputPath)/output_%v.m3u8"
    """

    print("[FFmpeg] Processing: \(file)")
    let process = Process()
    process.launchPath = "/bin/bash"
    process.arguments = ["-c", command]
    process.launch()
    process.waitUntilExit()
    print("[FFmpeg] Completed: \(file)")
}

print("[FFmpeg] The conversion process is all complete!")
