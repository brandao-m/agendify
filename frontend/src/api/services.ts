export async function getServices(tenantId: number) {

    const response = await fetch(
        `http://127.0.0.1:8000/services/?tenant_id=${tenantId}`
    );

    if (!response.ok) {
        throw new Error("Erro ao buscar serviços");
    }

    return response.json();
}