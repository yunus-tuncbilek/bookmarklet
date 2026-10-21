# Shufflemark

<img src="icon.svg" alt="Shufflemark logo" width="64">

A bookmark that plays a random video from a YouTube playlist. Free and open
source.

## How to use it (no technical skills needed)

1. Open the Shufflemark page: https://yunus-tuncbilek.github.io/shufflemark/
2. In YouTube, open your playlist and copy its link from the address bar (in
   the YouTube app: Share, then Copy link).
3. Paste the link into the box on the Shufflemark page. A blue box shows your
   personal Shufflemark link.
4. Bookmark that link (Ctrl+D, or ⌘+D on a Mac; on a phone, use the browser's
   Share or menu button and choose Add Bookmark).
5. Whenever you open the bookmark, a random video from your playlist starts.

The bookmark looks like this, if you'd rather build it by hand:

```
https://yunus-tuncbilek.github.io/shufflemark/?list=<playlist id>
```

Visitors don't need their own API key. The site uses one shared key.

- **Desktop:** the page redirects straight to a random video.
- **Phone/tablet:** the page shows an **Open in YouTube** button. Tapping it
  opens the video in the YouTube app (see below for why it's a button).
- **Caching:** the video IDs are cached in `localStorage` for 24 hours, so most
  clicks don't call the API. Private and deleted videos are skipped.

## Technical details

### Hosting setup

The page is deployed by
[`.github/workflows/pages.yml`](.github/workflows/pages.yml), which replaces
the `__YT_API_KEY__` placeholder in `index.html` with the key from a
repository secret. The key is never in the repo.

1. In Google Cloud Console, enable **YouTube Data API v3** and create an API
   key. Restrict it to websites `https://yunus-tuncbilek.github.io/*` and to the
   YouTube Data API v3.
2. In the repo, go to **Settings → Secrets and variables → Actions** and add a
   repository secret named `YT_API_KEY` containing the key.
3. Go to **Settings → Pages** and set **Source** to **GitHub Actions**.
4. Push to `master` (or run the workflow by hand from the Actions tab).

The deployed page contains the key, since the browser calls the API directly.
This is normal for browser API keys: the website restriction stops other sites
from using it. The free quota is 10,000 units a day and a playlist costs one
unit per 50 videos, so with the 24-hour cache it goes a long way.

### Why an API key is required

Opening a YouTube URL with a playlist id and a random index doesn't launch 
the video of the given index. For instance, something like this doesn't work:

```
https://www.youtube.com/watch?list=<playlist id>&index=<n>
```

Without a `v=` (video ID) parameter, YouTube shows a blank player with the
message "YouTube is not currently available on this device". This was tested by
hand in a browser on 2026-10-18. A
[GameRevolution article](https://www.gamerevolution.com/?p=676321) describes the
same behavior; YouTube has not documented it officially. So the page needs real
video IDs, which it gets from the YouTube Data API.

### Why mobile gets a button

On iOS, a `youtube.com` link opens the YouTube app through Apple's *universal
links*, but only when the user started the navigation by tapping something. A
redirect the page does by itself stays in Safari. Android's app links behave
similarly. So on phones and tablets the page waits for a tap on
**Open in YouTube** instead of redirecting.
