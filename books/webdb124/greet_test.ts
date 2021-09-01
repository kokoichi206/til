import { createApp } from "./create_greet_app.ts";
import { superoak } from "https://deno.land/x/superoak@4.4.0/mod.ts";

const app = createApp();

Deno.test(`GET /greet に対して、ステータスコード200で"Hellow anonymous!"が帰ってくること`, async() =>{
    const request = await superoak(app);
    await request.get("/greet").expect(200).expect("Hellow anonymous!");
});

// $ deno run --allow-net greet_test.ts
