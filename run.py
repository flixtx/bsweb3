from mediaflow_proxy.main import app
import uvicorn

if __name__ == "__main__":
    print("🚀 Iniciando MediaFlow Proxy na porta 8080")
    print("🌐 Acesse: http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
