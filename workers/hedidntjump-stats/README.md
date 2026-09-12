# hedidntjump-stats

Cloudflare Worker + KV counters for [hedidntjump.com](https://hedidntjump.com).

## Endpoints

| Method | Path | Action |
| --- | --- | --- |
| `GET` | `/api/stats` or `/stats` | Read totals. Does not increment. |
| `GET`/`POST` | `/api/hit?type=view\|download&id=...` | Increment and return totals. |

`POST` may send JSON `{ "type": "download", "id": "volume-1" }`.

CORS is open to `hedidntjump.com`, `*.pages.dev`, and `localhost`.

## Deploy

```bash
npx wrangler deploy
```

Expected workers.dev host (this account’s subdomain):

`https://hedidntjump-stats.vibelock.workers.dev`

The static site reads that URL from `<meta name="hdj-stats-api">` in `dist/index.html` / `dist/reader.html`. After deploy, live pills on GitHub Pages will increment.

KV namespace `HEDIDNTJUMP_STATS` (`1917a6bc70804f6f927d29598264e092`) is already bound as `STATS`.

## Local

```bash
npx wrangler dev
```

Then open the archive with the meta tag pointed at `http://localhost:8787`.
