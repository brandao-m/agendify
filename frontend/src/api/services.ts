export async function getServices() {
    const response = await fetch(
        'http://127.0.0.1:8000/services/?tenant_id=1'
    );

    if (!response.ok) {
        throw new Error('Erro ao buscar serviços');
    }

    return response.json();
}