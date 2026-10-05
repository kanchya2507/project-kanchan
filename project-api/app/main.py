from datetime import datetime, timezone
import html
import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.rag.routes import router as interview_router

APP_VERSION = os.getenv("APP_VERSION", "3.0.0")
BUILD_SHA = os.getenv("BUILD_SHA", "local/dev")
APP_STARTED_AT = datetime.now(timezone.utc).isoformat(timespec="seconds")

app = FastAPI(
    title="FastAPI Control Center",
    description="Deployment verification dashboard and application API",
    version=APP_VERSION,
)

USERS = [
    {"id": 1, "name": "Ava Patel", "email": "ava@example.com", "role": "Admin", "status": "Active"},
    {"id": 2, "name": "Noah Kim", "email": "noah@example.com", "role": "Editor", "status": "Active"},
    {"id": 3, "name": "Mia Garcia", "email": "mia@example.com", "role": "Viewer", "status": "Pending"},
    {"id": 4, "name": "Leo Chen", "email": "leo@example.com", "role": "Editor", "status": "Active"},
]

app.include_router(
    interview_router,
    prefix="/api/interview",
    tags=["DevOps interviewer"],
)

@app.get("/", response_class=HTMLResponse)
def root_dashboard():
    page = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>FastAPI Control Center</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #0b1020;
      --panel: #121a2d;
      --panel-light: #19243a;
      --text: #eef3ff;
      --muted: #98a7c2;
      --line: rgba(255,255,255,.09);
      --cyan: #56e0d1;
      --purple: #9b8cff;
      --green: #6ee7a8;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      background:
        radial-gradient(ellipse at 70% -15%, rgba(104,91,255,.22), transparent 45%),
        radial-gradient(ellipse at 5% 30%, rgba(39,205,190,.10), transparent 35%),
        var(--bg);
      color: var(--text);
      font: 15px/1.5 Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    }
    button { font: inherit; }
    .layout { display: grid; grid-template-columns: 240px 1fr; min-height: 100vh; }
    aside { padding: 28px 18px; border-right: 1px solid var(--line); background: rgba(11,16,32,.72); }
    .brand { display:flex; align-items:center; gap:12px; padding: 0 10px 34px; font-weight:800; letter-spacing:.2px; }
    .brand-mark {
      width:38px; height:38px; display:grid; place-items:center; border-radius:13px;
      background:linear-gradient(135deg,var(--cyan),var(--purple)); color:#08111e; font-size:20px;
    }
    .nav-label { padding: 0 12px; margin: 18px 0 8px; color:#70809e; font-size:11px; font-weight:800; letter-spacing:1.5px; text-transform:uppercase; }
    .nav-item { display:flex; gap:12px; align-items:center; padding:11px 12px; margin:4px 0; color:var(--muted); border-radius:11px; text-decoration:none; }
    .nav-item.active, .nav-item:hover { background:rgba(155,140,255,.13); color:#fff; }
    .nav-item span:first-child { width:20px; text-align:center; }
    .side-card { margin-top:38px; padding:15px; border:1px solid var(--line); border-radius:15px; background:linear-gradient(145deg,rgba(86,224,209,.08),rgba(155,140,255,.08)); }
    .side-card small { color:var(--muted); }
    main { width:min(1450px,100%); margin:auto; padding:32px clamp(20px,4vw,58px) 50px; }
    .topbar { display:flex; align-items:center; justify-content:space-between; gap:18px; margin-bottom:34px; }
    .crumb { color:var(--muted); font-size:13px; }
    .profile { display:flex; align-items:center; gap:10px; color:var(--muted); }
    .avatar { display:grid; place-items:center; width:36px; height:36px; border-radius:50%; background:#283550; color:var(--cyan); font-weight:800; }
    .hero { display:flex; justify-content:space-between; align-items:flex-end; gap:25px; margin-bottom:25px; }
    h1 { margin:5px 0 7px; font-size:clamp(30px,4vw,46px); line-height:1.1; letter-spacing:-1.7px; }
    .subtitle { margin:0; color:var(--muted); }
    .eyebrow { color:var(--cyan); font-size:12px; font-weight:800; letter-spacing:1.6px; text-transform:uppercase; }
    .button { padding:10px 15px; border:1px solid var(--line); border-radius:10px; background:var(--panel-light); color:var(--text); cursor:pointer; }
    .button:hover { border-color:var(--cyan); }
    .button.primary { background:linear-gradient(120deg,#53d9ca,#8275ed); color:#08111e; border:0; font-weight:800; }
    .grid { display:grid; gap:16px; }
    .metrics { grid-template-columns:repeat(4,minmax(0,1fr)); margin:24px 0; }
    .card { border:1px solid var(--line); border-radius:17px; background:linear-gradient(145deg,rgba(25,36,58,.96),rgba(17,25,43,.96)); box-shadow:0 16px 45px rgba(0,0,0,.12); }
    .metric { padding:19px; }
    .metric-head { display:flex; justify-content:space-between; align-items:center; color:var(--muted); font-size:13px; }
    .metric-icon { display:grid; place-items:center; width:34px; height:34px; border-radius:10px; background:rgba(86,224,209,.11); color:var(--cyan); }
    .metric-value { margin:13px 0 2px; font-size:29px; font-weight:800; letter-spacing:-.8px; }
    .metric-note { color:var(--green); font-size:12px; }
    .content-grid { grid-template-columns:1.5fr 1fr; }
    .section { padding:22px; }
    .section-title { display:flex; justify-content:space-between; align-items:center; gap:12px; margin-bottom:20px; }
    h2 { margin:0; font-size:17px; }
    .muted { color:var(--muted); font-size:13px; }
    .chart { width:100%; height:210px; overflow:visible; }
    .chart-labels { display:flex; justify-content:space-between; color:#7786a2; font-size:11px; }
    .service { display:flex; justify-content:space-between; gap:15px; align-items:center; padding:13px 0; border-bottom:1px solid var(--line); }
    .service:last-child { border-bottom:0; }
    .service-name { display:flex; align-items:center; gap:11px; }
    .service-icon { display:grid; place-items:center; width:34px; height:34px; border-radius:10px; background:#202d45; }
    .status { display:inline-flex; align-items:center; gap:7px; color:var(--green); font-size:12px; }
    .dot { width:7px; height:7px; border-radius:50%; background:currentColor; box-shadow:0 0 12px currentColor; }
    .deployment { margin-top:16px; padding:17px; border-radius:13px; background:rgba(86,224,209,.06); border:1px solid rgba(86,224,209,.14); }
    code { color:#b8adff; overflow-wrap:anywhere; }
    .users { margin-top:16px; }
    .table-wrap { overflow-x:auto; }
    table { width:100%; border-collapse:collapse; text-align:left; white-space:nowrap; }
    th { padding:11px 9px; color:#8291ad; font-size:11px; letter-spacing:1px; text-transform:uppercase; }
    td { padding:13px 9px; border-top:1px solid var(--line); color:#dce5f7; }
    .user-cell { display:flex; align-items:center; gap:10px; }
    .user-avatar { display:grid; place-items:center; width:32px; height:32px; border-radius:10px; background:#283550; color:var(--purple); font-weight:700; }
    .pill { padding:4px 9px; border-radius:20px; background:rgba(110,231,168,.1); color:var(--green); font-size:11px; }
    .pill.pending { background:rgba(255,197,99,.1); color:#ffc563; }
    .footer { margin-top:22px; color:#73819b; font-size:12px; text-align:center; }
    @media(max-width:950px) { .metrics{grid-template-columns:repeat(2,1fr)} .content-grid{grid-template-columns:1fr} }
    @media(max-width:650px) {
      .layout{grid-template-columns:1fr} aside{display:none} main{padding:22px 16px}
      .hero{align-items:flex-start; flex-direction:column} .topbar{margin-bottom:25px}
      .metrics{gap:10px} .metric{padding:14px} .metric-value{font-size:24px}
    }
  </style>
</head>
<body>
<div class="layout">
  <aside>
    <div class="brand"><div class="brand-mark">⚡</div><div>Pulse<span style="color:#56e0d1">API</span></div></div>
    <div class="nav-label">Workspace</div>
    <a class="nav-item active" href="#"><span>▦</span> Overview</a>
    <a class="nav-item" href="#services"><span>◈</span> Services</a>
    <a class="nav-item" href="#users"><span>♙</span> Users</a>
    <div class="nav-label">System</div>
    <a class="nav-item" href="#deployment"><span>⌁</span> Deployment</a>
    <a class="nav-item" href="/docs"><span>⌘</span> API Docs</a>
    <div class="side-card">
      <div style="font-weight:700;margin-bottom:5px">Deployment check</div>
      <small>Dashboard is served by your FastAPI container.</small>
      <div style="margin-top:13px" class="status"><span class="dot"></span> Live application</div>
    </div>
  </aside>

  <main>
    <div class="topbar">
      <div class="crumb">Workspace &nbsp;/&nbsp; <span style="color:#eef3ff">Overview</span></div>
      <div class="profile"><span>FastAPI environment</span><div class="avatar">F</div></div>
    </div>

    <section class="hero">
      <div>
        <div class="eyebrow">Application overview</div>
        <h1>Control Center</h1>
        <p class="subtitle">A live view of your API, service health, and deployed release.</p>
      </div>
      <button id="refresh-status" class="button primary" type="button">↻ &nbsp; Refresh status</button>
    </section>

    <section class="grid metrics">
      <div class="card metric"><div class="metric-head">API status <span class="metric-icon">◉</span></div><div class="metric-value" id="api-status">Checking</div><div class="metric-note">● Live health endpoint</div></div>
      <div class="card metric"><div class="metric-head">API version <span class="metric-icon">⌘</span></div><div class="metric-value">v__VERSION__</div><div class="metric-note">FastAPI application</div></div>
      <div class="card metric"><div class="metric-head">Registered users <span class="metric-icon">♙</span></div><div class="metric-value">04</div><div class="metric-note">Sample API data</div></div>
      <div class="card metric"><div class="metric-head">Environment <span class="metric-icon">◇</span></div><div class="metric-value" style="font-size:24px">ECS Ready</div><div class="metric-note">Containerized service</div></div>
    </section>

    <section class="grid content-grid">
      <div class="card section">
        <div class="section-title"><div><h2>Request activity</h2><div class="muted">Illustrative dashboard chart</div></div><span class="pill">Last 7 days</span></div>
        <svg class="chart" viewBox="0 0 700 210" preserveAspectRatio="none" role="img" aria-label="Illustrative request activity chart">
          <defs><linearGradient id="fill" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#56e0d1" stop-opacity=".32"/><stop offset="1" stop-color="#56e0d1" stop-opacity="0"/></linearGradient></defs>
          <g stroke="rgba(255,255,255,.08)" stroke-dasharray="4 7"><path d="M0 35H700"/><path d="M0 80H700"/><path d="M0 125H700"/><path d="M0 170H700"/></g>
          <path d="M0 160 C45 145 55 120 100 132 S160 165 205 112 S265 82 310 105 S370 140 415 78 S475 95 520 62 S585 80 630 42 S675 54 700 24 L700 200 L0 200Z" fill="url(#fill)"/>
          <path d="M0 160 C45 145 55 120 100 132 S160 165 205 112 S265 82 310 105 S370 140 415 78 S475 95 520 62 S585 80 630 42 S675 54 700 24" fill="none" stroke="#56e0d1" stroke-width="3"/>
        </svg>
        <div class="chart-labels"><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span></div>
      </div>

      <div class="card section" id="services">
        <div class="section-title"><div><h2>Service health</h2><div class="muted">Live endpoint checks</div></div></div>
        <div class="service"><div class="service-name"><span class="service-icon">⚡</span><div><strong>FastAPI service</strong><div class="muted">Application process</div></div></div><span class="status"><span class="dot"></span><span id="service-status">Checking</span></span></div>
        <div class="service"><div class="service-name"><span class="service-icon">♥</span><div><strong>Health endpoint</strong><div class="muted">GET /health</div></div></div><span class="status"><span class="dot"></span>Available</span></div>
        <div class="service"><div class="service-name"><span class="service-icon">⌘</span><div><strong>Interactive docs</strong><div class="muted">OpenAPI /docs</div></div></div><a class="muted" href="/docs">Open ↗</a></div>
        <div class="deployment" id="deployment">
          <div class="muted">RUNNING BUILD</div>
          <div style="margin:6px 0"><code>__BUILD_SHA__</code></div>
          <div class="muted">Container started: <span id="started-at">Loading…</span></div>
        </div>
      </div>
    </section>

    <section class="card section users" id="users">
      <div class="section-title"><div><h2>Team members</h2><div class="muted">Sample data from <code>/api/users</code></div></div><button id="reload-users" class="button" type="button">Reload users</button></div>
      <div class="table-wrap"><table><thead><tr><th>Member</th><th>Role</th><th>Status</th><th>Account</th></tr></thead><tbody id="user-rows"><tr><td colspan="4" class="muted">Loading users…</td></tr></tbody></table></div>
    </section>
    <div class="footer">FastAPI Control Center &nbsp;·&nbsp; Build __BUILD_SHA__ &nbsp;·&nbsp; <span id="footer-time"></span></div>
  </main>
</div>
<script>
  async function refreshStatus() {
    const status = document.getElementById("api-status");
    const serviceStatus = document.getElementById("service-status");

    status.textContent = "Checking";
    try {
      const response = await fetch("/health", { cache: "no-store" });
      if (!response.ok) throw new Error(`Health request failed: ${response.status}`);

      const data = await response.json();
      status.textContent = "Healthy";
      serviceStatus.textContent = "Operational";
      document.getElementById("started-at").textContent =
        new Date(data.started_at).toLocaleString();
    } catch (error) {
      status.textContent = "Offline";
      serviceStatus.textContent = "Unavailable";
      console.error("Could not refresh health status:", error);
    }
  }

  async function loadUsers() {
    const target = document.getElementById("user-rows");
    target.innerHTML = '<tr><td colspan="4" class="muted">Loading users…</td></tr>';

    try {
      const response = await fetch("/api/users", { cache: "no-store" });
      if (!response.ok) throw new Error(`Users request failed: ${response.status}`);

      const users = await response.json();
      target.innerHTML = users.map(user => `
        <tr>
          <td>
            <div class="user-cell">
              <div class="user-avatar">${user.name.split(" ").map(part => part[0]).join("")}</div>
              <div><strong>${user.name}</strong><div class="muted">${user.email}</div></div>
            </div>
          </td>
          <td>${user.role}</td>
          <td><span class="pill ${user.status === "Pending" ? "pending" : ""}">${user.status}</span></td>
          <td class="muted">#${user.id.toString().padStart(4, "0")}</td>
        </tr>
      `).join("");
    } catch (error) {
      target.innerHTML = '<tr><td colspan="4" class="muted">Could not load users. Check the API.</td></tr>';
      console.error("Could not load users:", error);
    }
  }

  document.getElementById("refresh-status").addEventListener("click", refreshStatus);
  document.getElementById("reload-users").addEventListener("click", loadUsers);

  document.getElementById("footer-time").textContent = new Date().toLocaleString();
  refreshStatus();
  loadUsers();
  setInterval(refreshStatus, 30000);
</script>
</body>
</html>
"""
    page = page.replace("__VERSION__", html.escape(APP_VERSION))
    page = page.replace("__BUILD_SHA__", html.escape(BUILD_SHA))
    return HTMLResponse(page)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": APP_VERSION,
        "build": BUILD_SHA,
        "started_at": APP_STARTED_AT,
    }


@app.get("/api/users")
def get_users():
    return USERS