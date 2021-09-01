import { Application, Router, helpers } from "https://deno.land/x/oak@v7.7.0/mod.ts";

// http://localhost:8888/greet?name=hoge
export function createApp(): Application {
    const app = new Application();
    const router = new Router();
    
    router.get("/greet", (ctx) => {
        const { name = "anonymous" } = helpers.getQuery(ctx);
        ctx.response.body = `Hello ${name}`;
    });

    app.use(router.routes());
    return app;
}
