# tommy-site

Personal website self-hosted on a Raspberry Pi. Built as a DevOps project.

## Stack

- **Frontend** — Static HTML with [BOOTSTRA.386](https://github.com/kristopolous/BOOTSTRA.386) (retro terminal aesthetic)
- **Backend** — FastAPI (Python), served via Uvicorn
- **Database** — SQLite (guestbook entries)
- **Web server** — Nginx (reverse proxy + static files)
- **Infrastructure** — Docker Compose on a Raspberry Pi
- **CI** — GitHub Actions (HTML validation, Python linting, Docker builds, backend tests)
- **Deploy** — Webhook-triggered `git pull` + `docker compose up`

## Pages

| Page | Description |
|------|-------------|
| `/` | Home |
| `/projects.html` | Data science & ML projects with notebook viewer |
| `/gym.html` | PRs and workout programs |
| `/food.html` | Dinner tracker (live from Google Sheets) + recipes |
| `/guestbook.html` | Public guest book |

## Project structure

```
frontend/        Static HTML, CSS, JS
  css/
    site.css     Global styles (layout, navbar, footer, viewer)
    food.css     Dinner chart + recipe viewer
    gym.css      PR grid + video viewer
    guestbook.css  Guest book form + entry cards
  js/
    components.js  Shared navbar + footer
backend/         FastAPI app
  app/main.py    API endpoints
nginx/           Nginx config + Dockerfile
deploy_webhook/  Webhook server for auto-deploy on push
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/dinners` | Dinner tracker data (Google Sheets) |
| GET | `/api/guestbook` | All guestbook entries |
| POST | `/api/guestbook` | Submit a guestbook entry |

