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

### Fix: `index.html` on GitHub Pages

`index.html` fetches the playlist with the YouTube Data API and opens a random video, so
nothing needs updating when the playlist changes. Bookmark it as a normal bookmark (not a
bookmarklet):

```
https://yunus-tuncbilek.github.io/bookmarklet/?list=<playlist id>
```

- **API key:** on first visit the page asks for a YouTube Data API key and stores it in a
  cookie in that browser for one year. The key is never in the repo. If the cookie expires
  or the API rejects the key, the page asks again.
- **Caching:** the video IDs are cached in `localStorage` for 24 hours, so most clicks don't
  call the API. Private and deleted videos are skipped.

Setup:
1. In Google Cloud Console, enable **YouTube Data API v3** and create an API key. Restrict
   it to websites `https://yunus-tuncbilek.github.io/*` and to the YouTube Data API v3.
2. In the repo's **Settings → Pages**, deploy from the `master` branch, `/ (root)` folder.

### iPad/iPhone: why it sometimes opens the YouTube app and sometimes Safari

On iOS, a `youtube.com` link opens the YouTube app through Apple's *universal links*. iOS
only does this when the user started the navigation by tapping something:

- **First visit:** you tapped **Save** in the API key form, and the redirect followed that
  tap, so iOS opened the YouTube app.
- **Later visits:** the key and playlist are already saved, so the page redirects by itself
  with no tap. iOS treats that as a script redirect and keeps it in Safari.

A second possible cause: if you ever choose to open a YouTube link in Safari instead (e.g. the
`youtube.com` link at the top right of the YouTube app), iOS remembers that and keeps opening
`youtube.com` links in Safari. Long-press a YouTube link and choose **Open in "YouTube"** to
switch it back.

This is an untested explanation based on how universal links behave. If the app is
preferred, the page could show an **Open video** button instead of redirecting automatically,
so the tap opens the app.
