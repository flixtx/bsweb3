from mediaflow_proxy.main import app
import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        workers=3,  # Mantém os workers do original
        log_level="info"
    )
