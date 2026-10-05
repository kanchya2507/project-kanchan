from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI(
    title="Production Project API",
    description="Enterprise FastAPI application running serverless on AWS ECS Fargate",
    version="2.0.0" # Bumped to a major release version!
)

@app.get("/", response_class=HTMLResponse) 
def root_dashboard():
    # A beautiful, modern styled HTML dashboard to immediately verify deployment success visually!
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI Enterprise Dashboard</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: #ffffff;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .card {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                padding: 40px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.2);
                text-align: center;
                max-width: 500px;
            }}
            h1 {{ margin-top: 0; color: #4facfe; font-size: 2.5em; }}
            .status-badge {{
                background-color: #00ff87;
                color: #121212;
                padding: 6px 16px;
                border-radius: 20px;
                font-weight: bold;
                display: inline-block;
                margin: 15px 0;
                box-shadow: 0 0 15px #00ff87;
            }}
            .meta {{ color: #e0e0e0; font-size: 0.95em; margin: 10px 0; }}
            .btn {{
                background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
                border: none;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
                text-decoration: none;
                display: inline-block;
                margin-top: 20px;
                box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
            }}
            .btn:hover {{ transform: translateY(-2px); transition: 0.2s; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 Deployment Live!</h1>
            <div class="status-badge">AWS ECS FARGATE: ACTIVE</div>
            <p style="font-size: 1.2em;">Hello from FastAPI! Your GitHub Actions CD pipeline successfully pushed this major update without a single second of downtime.</p>
            <div class="meta"><strong>API Version:</strong> 2.0.0</div>
            <div class="meta"><strong>Last Engine Sync:</strong> {current_time}</div>
            <a href="/docs" class="btn">Explore Interactive Swagger Docs</a>
        </div>
    </body>
    </html>
    """

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "infra": "AWS ECS Fargate",
        "load_balancer": "Application Load Balancer",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/users")
def get_users():
    return {
        "total_count": 5,
        "department": "Engineering & DevOps",
        "users": [
            {"id": 1, "name": "Rohit", "role": "Backend Engineer"},
            {"id": 2, "name": "Amit", "role": "Frontend Lead"},
            {"id": 3, "name": "Priya", "role": "QA Architect"},
            {"id": 4, "name": "Kanchan", "role": "DevOps / Pipeline Owner"},
            {"id": 5, "name": "AWS-Fargate-Bot", "role": "Serverless Automated Runner"}
        ]
    }
