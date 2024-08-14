/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Bind resources to your worker in `wrangler.toml`. After adding bindings, a type definition for the
 * `Env` object can be regenerated with `npm run cf-typegen`.
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

export default {
	async fetch(request, env, ctx): Promise<Response> {
		const url = new URL(request.url);
		const path = url.pathname;

		if (path === '/lh') {
			const res = await fetch('http://localhost:8080', {
				method: 'GET',
			});
			console.log(res);
			console.log(await res.text());
			return new Response(`${await res.text()}! in lh`, {
				headers: { 'content-type': 'text/plain' },
			});
		} else if (path === '/0000') {
			const res = await fetch('http://0.0.0.0:8080', {
				method: 'GET',
			});
			console.log(res);
			console.log(await res.text());
			return new Response(`${await res.text()}! in 0000`, {
				headers: { 'content-type': 'text/plain' },
			});
		} else {
			return new Response('404 Not Found', {
				status: 404,
				headers: { 'content-type': 'text/plain' },
			});
		}
	},
} satisfies ExportedHandler<Env>;
