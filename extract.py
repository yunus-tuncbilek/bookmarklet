''' 
instructions: This script extracts video IDs from a YouTube playlist 
   and updates the `episodes` variable in `conan.js`.
'''

import yt_dlp

# Replace with your playlist URL
playlist_url = 'https://www.youtube.com/playlist?list=PL2LQfBmxWgZaK0_rf64Vm_ude4YmHOC1m' 

video_ids = []
try:
    ydl_opts = {
        'quiet': True,
        'verbose': False,
        'no_warnings': True,
        'extract_flat': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        for entry in info.get('entries', []):
            video_ids.append(entry['id'])
    print(f"Extracted {len(video_ids)} video IDs from the playlist.")
except Exception as e:
    print(f"An error occurred while fetching playlist info: {e}")
    exit(1)

# --- Update episodes variable in conan.js ---
import re

try:
    with open('conan.js', 'r') as js_file:
        js_content = js_file.read()

    # Replace the episodes variable (assumes: let episodes = [...] or var episodes = [...] or const episodes = [...])
    new_js_content = re.sub(
        r'(let|var|const)\s+episodes\s*=\s*\[.*?\];',
        f'let episodes = {video_ids};',
        js_content,
        flags=re.DOTALL
    )

    with open('conan.js', 'w') as js_file:
        js_file.write(new_js_content)

    print("conan.js updated successfully.")
except FileNotFoundError:
    print("Error: The file 'conan.js' was not found.")
except Exception as e:
    print(f"An error occurred while updating conan.js: {e}")