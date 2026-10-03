<!-- LOVABLE:BEGIN -->
> [!IMPORTANT]
> This project is connected to [Lovable](https://lovable.dev). Avoid rewriting
> published git history — force pushing, or rebasing/amending/squashing commits
> that are already pushed — as it rewrites history on Lovable's side and the
> user will likely lose their project history.
>
> Commits you push to the connected branch sync back to Lovable and show up in
> the editor, so keep the branch in a working state.
<!-- LOVABLE:END -->

## Project rules

- READ `HANDOFF.md` first; "أكمل" = continue its remaining product videos, 3 per batch.
- Fonts are self-hosted in `public/fonts/` via `/fonts/fonts.css` in `src/routes/__root.tsx` — no external font requests.
- All runtime media resolves to local paths (`/videos`, `/media`, `/catalogs`, `/fonts`, `/brand`) — never `/__l5e/` CDN or remote hosts, so the desktop app runs offline.
- Repo files stay under 10 MB: bigger videos live split in `public/videos/parts/`, reassembled by `src/lib/video-source.ts`; keep original 1080p quality, never transcode.
- Windows desktop app is a lightweight Neutralino (WebView2) shell loading the published site (`desktop-lite/`, zip in `public/downloads/`) — keeps the download under 40 MB and always up to date.
- Products catalog (`src/lib/products-data.ts` + `src/components/products-catalog.tsx`) is information-only: no pricing, ordering or quote flows linked into it.
- Product intro videos are real `<video>` files in `src/lib/product-video.ts`, played by `src/components/product-video.tsx` — never slideshows or CSS-animated stills.
- Specs, compatibility and images come only from bundled catalogs or the manufacturer's official sources — never guess or reuse a similar model's image.
- Except solar panels, every showroom product sits on the standard white podium at catalog-documented proportions; regenerate video from the corrected still.
- SLD cable-size edits are presentation-only overrides passed into calculation helpers; the quote-derived system model stays immutable.
