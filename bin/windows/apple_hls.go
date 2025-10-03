package main

import ("fmt""log""os""os/exec""path/filepath""strings")

func main() {
	baseDir, err := os.Getwd()
	if err != nil {
		log.Fatalf("Failed to get current directory: %v", err)
	}

	inputFolder := filepath.Join(baseDir, "assets", "video")
	outputFolder := filepath.Join(baseDir, "assets", "stream")

	// Create the original output directory if it does not exist
	if err := os.MkdirAll(outputFolder, 0755); err != nil {
		log.Fatalf("Failed to create output folder: %v", err)
	}

	files, err := os.ReadDir(inputFolder)
	if err != nil {
		log.Fatalf("Failed to read input folder: %v", err)
	}

	for _, file := range files {
		if file.IsDir() {
			continue
		}

		name := file.Name()
		if !strings.HasSuffix(strings.ToLower(name), ".mp4") && !strings.HasSuffix(strings.ToLower(name), ".mov") {
			fmt.Printf("Skipping unsupported file: %s\n", name)
			continue
		}

		inputFilePath := filepath.Join(inputFolder, name)
		fileName := strings.TrimSuffix(name, filepath.Ext(name))
		outputPath := filepath.Join(outputFolder, fileName)

		// If output folder exists => skip
		if _, err := os.Stat(outputPath); err == nil {
			fmt.Printf("Skipping: Folder '%s' exists. Do not process file: '%s'.\n", outputPath, name)
			continue
		}

		if err := os.MkdirAll(outputPath, 0755); err != nil {
			log.Fatalf("Failed to create output path: %v", err)
		}

		fmt.Printf("[FFmpeg] Processing: %s\n", name)

		cmd := exec.Command(
			"ffmpeg",
			"-i", inputFilePath,
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
			"-hls_segment_filename", filepath.Join(outputPath, "output_%v_%03d.ts"),
			"-master_pl_name", "master.m3u8",
			filepath.Join(outputPath, "output_%v.m3u8"),
		)

		// Attach stdout/stderr to watch live ffmpeg progress
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr

		if err := cmd.Run(); err != nil {
			log.Fatalf("FFmpeg failed for file %s: %v", name, err)
		}

		fmt.Printf("[FFmpeg] Completed: %s\n", name)
	}

	fmt.Println("[FFmpeg] All conversions complete!")
}
