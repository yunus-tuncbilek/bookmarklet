# bookmarklet

`conan.js` is a Firefox bookmarklet that opens a random episode from a YouTube playlist.
The episode list is hardcoded, so whenever the playlist changes you have to run
`extract.py` (uses `yt-dlp`) and paste the updated `conan.js` back into the bookmark.

## Notes

### Picking a random video by index doesn't work

One idea for skipping the extract step was to store only the playlist ID and video count,
and open a URL with a random index instead of a video ID:

```
https://www.youtube.com/watch?list=<playlist id>&index=<n>
```

This doesn't work. Without a `v=` (video ID) parameter, YouTube shows a blank player with
the message "YouTube is not currently available on this device". This was tested by hand in
a browser on 2026-10-18. A [GameRevolution article](https://www.gamerevolution.com/?p=676321)
describes the same behavior; YouTube has not documented it officially.

So the bookmarklet needs real video IDs, which means either keeping the hardcoded list or
fetching the playlist with the YouTube Data API.

### Possible fix: YouTube Data API

Calling the API from the bookmarklet itself is unreliable: many sites' Content Security
Policy blocks the request, and the API key can't be restricted to a referrer. A better
option is a static page on GitHub Pages, opened from a plain bookmark such as
`https://<user>.github.io/bookmarklet/?list=<playlist id>`. The page would fetch
`playlistItems.list` (50 items per request), skip private and deleted videos, cache the IDs
in `localStorage`, and redirect to `watch?v=<random id>&list=<playlist id>`.
