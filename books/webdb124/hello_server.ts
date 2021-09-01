import { Application } from "https://deno.land/x/oak@v7.7.0/mod.ts";

const app = new Application();

app.use((ctx) => {
    ctx.response.body = "Hellow World!";
});

await app.listen({ port: 8888 });
