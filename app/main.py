from fastapi import FastAPI

app = FastAPI(
    title='Agendify API',
    version='0.1.0'
)

@app.get('/')
def root():
    return {'message': 'app rodando.'}