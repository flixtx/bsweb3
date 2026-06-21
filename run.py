from fastapi import FastAPI, APIRouter
import sys

try:
    from mediaflow_proxy.main import app as mediaflow_app
except ImportError:
    print("Erro: mediaflow_proxy não está instalado")
    print("Instale usando: pip install mediaflow-proxy")
    sys.exit(1)

# Inicializa a aplicação principal
main_app = FastAPI(
    title="MediaFlow Proxy Wrapper",
    description="Aplicação wrapper para MediaFlow Proxy",
    version="1.0.0"
)

# Cria um novo router
clean_router = APIRouter()

# Itera sobre as rotas do mediaflow_app
for route in mediaflow_app.router.routes:
    try:
        # Obtém o nome da rota
        route_name = getattr(route, 'name', '')
        route_path = getattr(route, 'path', '')
        
        # Pula a rota estática problemática
        if route_name == 'static':
            print(f"Pulando rota estática: {route_path}")
            continue
        
        # Pula rotas vazias
        if not route_path and not route_name:
            print("Pulando rota sem path e sem nome")
            continue
        
        # Adiciona a rota ao router limpo
        clean_router.routes.append(route)
        print(f"Rota adicionada: {route_path} ({route_name})")
        
    except Exception as e:
        print(f"Erro ao processar rota: {e}")
        continue

# Inclui o router limpo na aplicação principal
main_app.include_router(clean_router)

# Endpoints personalizados
@main_app.get("/health")
async def health_check():
    return {"status": "saudável", "serviço": "mediaflow-proxy-wrapper"}

@main_app.get("/")
async def root():
    return {
        "mensagem": "MediaFlow Proxy Wrapper",
        "rotas": f"{len(main_app.routes)} rotas carregadas",
        "status": "online"
    }

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
    return {"total": len(routes), "rotas": routes}

if __name__ == "__main__":
    import uvicorn
    print(f"\n{'='*50}")
    print(f"MediaFlow Proxy Wrapper iniciado")
    print(f"Total de rotas: {len(main_app.routes)}")
    print(f"{'='*50}\n")
    uvicorn.run(
        main_app, 
        host="0.0.0.0", 
        port=8080,
        log_level="info",
        access_log=True
    )
