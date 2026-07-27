# Phishing Detector — Frontend

A React (Vite) + Tailwind CSS single-page app that talks to the FastAPI backend in this repo. Three pages:

| Page          | Route        | Backend call        | Access | What it does |
|---------------|--------------|---------------------|--------|--------------|
| URL Checker   | `/`          | `POST /api/predict` | Public | Type a URL → Safe/Phishing result with a confidence bar. |
| Dashboard     | `/dashboard` | `GET /api/metrics`  | Public | Stat cards (total, phishing, detection rate) + Safe-vs-Phishing donut chart. |
| Logs          | `/logs`      | `GET /api/logs`     | **Admin only** | Searchable, filterable table of every past check. Requires admin login. |

## Admin authentication (username + password + JWT)

The **Logs** page is restricted to an admin. Security is enforced in two places:

1. **Backend** — `POST /api/login` checks the credentials against env vars and returns a signed **JWT**. `GET /api/logs` requires that token (`Authorization: Bearer …`); a direct `curl` without it is rejected with `401`. Hiding the page alone would not be secure.
2. **Frontend** — the `/logs` page shows a login form until the admin signs in; the JWT is then stored and attached to log requests.

The URL Checker and Dashboard stay public. No external service, OAuth app, or client ID is required.

### Configure the credentials

Set these in the repo-root `.env` (used by docker-compose — see [../README.md](../README.md)):

```bash
# ../.env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-me           # CHANGE THIS
JWT_SECRET=a-long-random-string    # CHANGE THIS — signs the session tokens
JWT_EXPIRE_HOURS=12                # session lifetime
```

Generate a strong secret with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Restart the backend after changing them: `docker compose up -d ml-service`.

## Run it — development

```bash
cd frontend
npm install
npm run dev
```

Open the URL Vite prints (usually `http://localhost:3000`, or the next free port). The backend must be running (`docker compose up -d` from the repo root).

> **CORS:** the backend only accepts browser requests from origins in its allow-list (`ALLOWED_ORIGINS`). Ports `8080`, `3000`, and `5173` (localhost + 127.0.0.1) are allowed by default. If Vite picks a different port, add that origin to `ALLOWED_ORIGINS` in the root `.env` and restart the backend.

## Run it — Docker (production-style)

The frontend has its own container (multi-stage: Vite build → nginx). From the repo root:

```bash
docker compose up --build -d
```

Served at **http://localhost:8080** (host `:3000` is often taken, so the frontend container publishes `8080`). Change the mapping in `docker-compose.yml` (`"8080:80"`) if you prefer another port — and add that origin to `ALLOWED_ORIGINS`.

## Point it at a different backend (e.g. Render)

`VITE_API_BASE_URL` controls the backend URL (baked at build time):

```bash
# root .env  (or frontend/.env for `npm run dev`)
VITE_API_BASE_URL=https://your-ml-service.onrender.com
```

Then rebuild. Also add your deployed frontend origin to the backend's `ALLOWED_ORIGINS`.

## Production build (static hosting, no container)

```bash
npm run build      # → dist/
npm run preview    # serve dist/ locally to check it
```

Deploy `dist/` to any static host (Netlify, Vercel, Render Static Site). Set `VITE_API_BASE_URL` in that host's build environment.

## Project structure

```
frontend/
├── Dockerfile              # multi-stage: node build → nginx serve
├── nginx.conf              # SPA fallback routing
├── vite.config.js          # React + Tailwind plugins, dev port 3000
├── .env                    # VITE_API_BASE_URL
├── public/shield.svg
└── src/
    ├── main.jsx            # entry: AuthProvider + Router
    ├── App.jsx             # layout + routes
    ├── api/client.js       # axios instance; attaches admin JWT to requests
    ├── auth/
    │   └── AuthContext.jsx # login/logout + JWT session state
    ├── components/
    │   ├── Navbar.jsx           # nav + signed-in admin badge / sign-out
    │   ├── StatCard.jsx
    │   └── LoginForm.jsx        # username/password form
    └── pages/
        ├── UrlChecker.jsx
        ├── Dashboard.jsx
        └── Logs.jsx        # admin-gated; shows login form until authorized
```

## Notes

- All backend calls live in `src/api/client.js`. A request interceptor attaches the stored JWT as `Authorization: Bearer …` to every request; only `/api/logs` requires it.
- If the token expires, the next `/api/logs` call returns `401`; the app clears the session and shows the login form again.
- The Dashboard donut sets `isAnimationActive={false}` on purpose: Recharts' enter animation renders an empty chart under React 18 StrictMode's double-mount.
