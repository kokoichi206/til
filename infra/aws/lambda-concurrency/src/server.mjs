import { createServer } from 'node:http';
import { work } from './shared.mjs';

// Shared by two runners: run locally with `node src/server.mjs`, and inside
// Lambda through the Web Adapter. The code is identical; only the substrate differs.
const PORT = Number(process.env.PORT ?? process.env.AWS_LWA_PORT ?? 8000);
const SLEEP_MS = Number(process.env.SLEEP_MS ?? 5000);

// The Web Adapter readiness probe must not run work(), or it would pollute the
// invocation/inFlight counters. It is routed to /healthz via AWS_LWA_READINESS_CHECK_PATH.
const server = createServer(async (req, res) => {
  if (req.url === '/healthz') {
    res.writeHead(200, { 'content-type': 'text/plain' });
    res.end('ok');
    return;
  }
  const result = await work(SLEEP_MS);
  res.writeHead(200, { 'content-type': 'application/json' });
  res.end(JSON.stringify({ runner: 'server', ...result }));
});

server.listen(PORT, () => {
  console.log(`listening on ${PORT} (sleepMs=${SLEEP_MS})`);
});
