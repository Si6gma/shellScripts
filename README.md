<!--
Suggested GitHub Topics:
shell-scripts, bash, automation, productivity, macos, home-automation, govee, cli-tools, youtube-dl, image-conversion, firebase, telemetry
-->

# shellScripts

A collection of personal shell scripts for macOS automation, productivity, media handling, IoT device control, and development workflows.

## 📜 Scripts Inventory

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `brw` | Updates, upgrades, and cleans Homebrew packages | Homebrew |
| `conv` | Converts HEIC images to JPEG format | ImageMagick |
| `copy` | Interactively copies contents of text files in a directory to clipboard | macOS `pbcopy` |
| `dog` | Keeps a local network device awake by pinging it every 15 seconds | curl |
| `mp3` | Downloads audio from YouTube videos and converts to MP3 | yt-dlp, ffmpeg |
| `pic` | Interactive image converter (PNG/JPG/PDF) | ImageMagick |
| `run` | Compiles and runs C programs (ARM64), auto-deletes binary after | gcc |
| `sshstart` | Starts SSH agent and adds the default SSH key | ssh-agent |
| `start` | Displays a colorful animated log from a file | - |
| `yt` | Downloads videos from YouTube in MP4 format | yt-dlp |

### IoT & Smart Home

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `brightness` | Sets brightness for Govee smart lights via API | curl, auth.sh (not included) |
| `lights` | Full-featured Govee light controller with presets | curl, jq, auth.sh (not included) |

### Development/Telemetry

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `hart` | Simulates and sends vehicle telemetry data to Firebase | curl, Node.js, generate-id-token.js (not included) |

## 🚀 Usage

### General Scripts

```bash
# Update Homebrew
./brw

# Convert HEIC images to JPEG
./conv /path/to/folder

# Copy text files to clipboard interactively
./copy

# Download YouTube video
./yt "https://youtube.com/..." "my_video"

# Download YouTube audio as MP3
./mp3 "https://youtube.com/..." "my_song"

# Convert image format
./pic input.jpg
# Then follow prompts for output format

# Compile and run C program
./run myprogram.c

# Start SSH agent
./sshstart
```

### Govee Light Control (Requires Setup)

**Note:** These scripts require `auth.sh` with your Govee API key and device IDs (see Security Notes).

```bash
# Set brightness for all lights
./brightness 50

# Turn on lights
./lights -o

# Apply a preset (sunset, ocean, brightwhite, test)
./lights -p sunset

# Set custom RGB color
./lights -d 1 -r 255 -g 0 -b 0
```

### Telemetry Script (Requires Setup)

**Note:** This script requires Firebase setup with `generate-id-token.js` (see Security Notes).

```bash
# Start sending simulated vehicle telemetry
./hart
```

## 🔒 Security Notes

Several scripts interact with external services that require authentication credentials:

### `brightness` and `lights` Scripts
- Require `auth.sh` containing `API_KEY` and `devices` array
- `auth.sh` is **gitignored** and must be created locally
- Obtain your API key from [Govee Developer Portal](https://developer.govee.com/)
- Example `auth.sh`:
  ```bash
  API_KEY="your-govee-api-key"
  devices=("device-id-1" "device-id-2" "device-id-3")
  ```

### `hart` Script
- Requires `generate-id-token.js` for Firebase authentication
- Connects to Firebase Realtime Database for telemetry simulation
- Designed for testing vehicle telemetry dashboards
- Authentication files are **gitignored**

### General Recommendations
- Never commit API keys, tokens, or credentials to git
- Use environment variables or separate auth files (already configured in `.gitignore`)
- The `.gitignore` already excludes:
  - `auth.sh`
  - `generate-id-token.js`
  - `firebase-service-account.json`
  - `logfile.txt`
  - Node.js artifacts

## 📋 Requirements

- macOS (uses `pbcopy`, `open` commands)
- Bash 4.0+
- Optional dependencies based on usage:
  - [Homebrew](https://brew.sh/)
  - [ImageMagick](https://imagemagick.org/)
  - [yt-dlp](https://github.com/yt-dlp/yt-dlp)
  - [ffmpeg](https://ffmpeg.org/)
  - [jq](https://stedolan.github.io/jq/)

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

These scripts are for personal use and learning purposes. Use at your own risk. Always review scripts before running them, especially those that modify system settings or interact with external APIs.
