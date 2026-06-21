from fastapi import FastAPI
import sys

# Tenta importar o mediaflow_proxy
try:
    from mediaflow_proxy.main import app as mediaflow_app
except ImportError:
    print("Erro: mediaflow_proxy não está instalado")
    print("Instale usando: pip install mediaflow-proxy")
    sys.exit(1)

# Inicializa a aplicação FastAPI principal
main_app = FastAPI(
    title="MediaFlow Proxy Wrapper",
    description="Aplicação wrapper para MediaFlow Proxy",
    version="1.0.0"
)

# Simplesmente inclui todo o router do mediaflow_app
# Isso lida com todos os tipos de rota automaticamente
main_app.include_router(mediaflow_app.router)

# Adiciona endpoints personalizados
@main_app.get("/health")
async def health_check():
    return {"status": "saudável", "serviço": "mediaflow-proxy-wrapper"}

@main_app.get("/routes")
async def list_routes():
    """Lista todas as rotas ativas para depuração"""
    routes = []
    for route in main_app.routes:
        if hasattr(route, 'path'):
            routes.append({
                "path": route.path,
                "methods": getattr(route, 'methods', ['GET']),
                "name": getattr(route, 'name', 'sem_nome')
            })
    return {"rotas": routes}

if __name__ == "__main__":
    import uvicorn
    print("Iniciando MediaFlow Proxy Wrapper...")
    print(f"Total de rotas carregadas: {len(main_app.routes)}")
    uvicorn.run(
        main_app, 
        host="0.0.0.0", 
        port=8080,
        log_level="info",
        access_log=True
    )
