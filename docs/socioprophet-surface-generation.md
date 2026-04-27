# SocioProphet surface generation

`SocioProphet/socioprophet` currently publishes the live surface source at:

- `config/surfaces.json`

That source is list-shaped and uses snake_case keys such as:

- `landing_page`
- `survey_page`
- `docs_path`
- `homepage_visible`
- `topic_constituents`
- `normalized_topics`
- `related_surfaces`
- `related_sites`
- `next_action`
- `investor_overlay.lens`

Use:

```bash
python scripts/generate_socioprophet_surfaces_from_config.py \
  ../socioprophet/config/surfaces.json \
  generated/socioprophet-surfaces.ttl
```

The older `scripts/generate_socioprophet_surfaces.py` scaffold is retained for compatibility, but this script is the canonical path for the current upstream `socioprophet` surface config shape.
