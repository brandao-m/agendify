from fastapi import FastAPI

from app.api.tenants import router as tenant_router 

app = FastAPI(
    title='Agendify API',
    version='0.1.0'
)

app.include_router(tenant_router)

@app.get('/')
def root():
    return {'message': 'app rodando.'}