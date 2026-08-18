import logging
import subprocess
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# Configure API logging to stdout and local file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/var/log/metrics-collector/metrics_api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("metrics_api")

app = FastAPI()

# Enable CORS for decoupled frontend environments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_system_command(command_list):
    """Helper to safely execute Linux system shell utilities."""
    try:
        result = subprocess.run(
            command_list, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return f"Error executing {' '.join(command_list)}:\n{result.stderr.strip()}"
    except Exception as e:
        return f"Execution failure: {str(e)}"

@app.middleware("http")
async def log_api_requests(request: Request, call_next):
    """Intercepts and logs API traffic and tracking variables."""
    logger.info(f"Incoming: {request.method} {request.url.path} | Client IP: {request.client.host}")
    response = await call_next(request)
    logger.info(f"Outgoing: Status {response.status_code}")
    return response

@app.get("/status")
def get_system_status():
    """Executes and formats requested core Linux utility readouts."""
    logger.info("Executing system status telemetry scripts.")
    
    # Run exact shell operations requested by client
    uname_data = run_system_command(["uname", "-a"])
    ip_data = run_system_command(["ip", "addr"])
    df_data = run_system_command(["df", "-h"])
    
    # Checking file permissions explicitly using ls -l on common targets
    ls_data = run_system_command(["ls", "-lrt", "/etc/passwd", "/etc/shadow", "/var/log"])

    return {
        "uname": uname_data,
        "ip_addr": ip_data,
        "df_h": df_data,
        "ls_lrt": ls_data
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Metrics API engine listening on port 6000.")
    # Port 6000 explicitly mapped to catch incoming proxy definitions
    uvicorn.run(app, host="0.0.0.0", port=6000)
