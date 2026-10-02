# Why We Become — Everyone Else Is Living Better

Narration-synchronized, motion-graphics-first video project.

## Watch

[Completed v2 release](https://github.com/xoloteach/why-we-become-everyone-else-living-better/releases/tag/v2-motion-37044793527)

The release contains `final-v2-motion.mp4`, thumbnail, SEO, transcript, panel synchronization review, source archive, and visual/technical QA. The previous v1 release is preserved.

## Reference output

- 1920 × 1080, 30 fps, 10:55.
- 90 artwork panels mapped into 109 narration-timed scenes.
- Twenty semantic graphic engines, neural 4× panel reconstruction, ink reveals, independently moving art layers, and phrase-timed labels.
- Word-highlighted captions and synchronized, ducked sound design.

## Reproduce the saved episode

Use the **Render motion rebuild v2** GitHub Actions workflow and its manual Run workflow action. The checked-in artwork and mastered narration are in `inputs/`; reproducing this saved episode does not require a new TTS request or a personal Notion login.

The workflow installs dependencies, prepares fonts/model and the expected `/data` layout, generates the narration map, reconstructs artwork, builds audio/captions, renders the full video, records QA, and publishes a new versioned release using the workflow's scoped GitHub token. Running this in a fork uses that fork's release destination. Never paste a personal access token into the workflow.

## Source map

- `v2/plan.py`: narration alignment, semantic scene plan, captions, timing review, and chapter SEO.
- `v2/upscale.py`: actual grid-boundary extraction, neural reconstruction, paper masks, and artwork metadata.
- `v2/prepare_audio.py`: cue-driven soundtrack preparation and efficient speech ducking.
- `v2/render_motion.py`: illustration compositing, typography, graphic engines, transitions, and video encoding.
- `.github/workflows/render-v2.yml`: persistent complete render and versioned release packaging.

The legacy `v2/finish.py` is local, workspace-specific orchestration, not the portable public reproduction entry point. Use the workflow above.

## Adapt to another video

Build a new narration/panel inventory and scene plan. Do not reuse this episode's hardcoded cue times or panel order for a different script. Preserve the semantic relationship between a spoken phrase, artwork, and the selected animation. Withhold future labels, wait for nodes before drawing their arrows, and keep exact count diagrams exact. Qualitative diagrams are not empirical measurements.

The current renderer is landscape-specific. A vertical adaptation needs native 1080 × 1920 layout, portrait extraction, readable stacked diagrams, mobile-safe caption/UI zones, and an aspect-preserving end card—not merely a resolution change or center crop.

## Verification and security

Inspect layout previews and actual captioned motion samples; check timing, masks, typography collisions, and sound. A contact sheet alone does not validate an entire animation. Neural upscaling is reconstruction, not guaranteed recovery of original detail.

Keep API keys, private workspace exports, `.env` files, and credential-bearing logs out of commits and release archives. Inspect history and archives before publication. Public visibility by itself is not a license grant for artwork, fonts, models, or code; respect their applicable terms.
