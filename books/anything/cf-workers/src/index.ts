import { Hono } from "hono";
import { basicAuth } from "hono/basic-auth";

const app = new Hono();

// // プロキシサーバーの設定が簡単に！
// app.all('*', (c) => fetch(c.req.raw))

app.get("/", (c) => {
  return c.text("Hello Hono!");
});

// basic 認証の追加。
app.use(
  "/auth/*",
  basicAuth({
    username: "hono",
    password: "pien",
  })
);
app.get("/auth", (c) => {
  return c.text("Hello Auth!");
});

export default app;
