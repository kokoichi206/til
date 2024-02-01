export async function onRequest(context) {
    const value = await context.env.KV.get('count');
    const currentCount = Number.isNaN(Number(value)) ? 0 : Number(value);
    const count = currentCount + 1;
    await context.env.KV.put('count', count);
    return Response.json({ count: count });
}
