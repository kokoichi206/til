// Fires N requests in parallel and aggregates the responses by envId.
//
// Usage: node driver/drive.mjs <baseUrl> [n=10] [label]
//
// A Function URL throttled by reserved concurrency returns HTTP 429. Lambda does
// not queue synchronous invocations, so the driver polls on 429 until a slot frees;
// this reproduces the serialized (~n * sleep) wall clock for concurrency = 1.
const [, , baseUrl, nArg, labelArg] = process.argv;

if (!baseUrl) {
  console.error('usage: node driver/drive.mjs <baseUrl> [n=10] [label]');
  process.exit(1);
}

const N = Number(nArg ?? 10);
const LABEL = labelArg ?? baseUrl;
const POLL_MS = 500;

async function fire(i) {
  const startedAt = Date.now();
  let attempts = 0;
  for (;;) {
    attempts += 1;
    const res = await fetch(baseUrl, { headers: { 'x-req': String(i) } });
    if (res.status === 429) {
      await new Promise((r) => setTimeout(r, POLL_MS));
      continue;
    }
    const body = await res.json();
    return { i, status: res.status, throttleWaits: attempts - 1, roundtripMs: Date.now() - startedAt, ...body };
  }
}

const startedAt = Date.now();
const results = await Promise.all(Array.from({ length: N }, (_, i) => fire(i)));
const totalMs = Date.now() - startedAt;

const byEnv = new Map();
for (const r of results) {
  const list = byEnv.get(r.envId) ?? [];
  list.push(r);
  byEnv.set(r.envId, list);
}

const maxInFlight = Math.max(...results.map((r) => r.maxInFlight));

console.log(`\n=== ${LABEL} ===`);
console.log(`requests           : ${N}`);
console.log(`total wall clock   : ${(totalMs / 1000).toFixed(2)} s`);
console.log(`distinct envIds    : ${byEnv.size}`);
console.log(`max inFlight (any) : ${maxInFlight}`);
console.log('per env:');
for (const [envId, list] of byEnv) {
  const maxIf = Math.max(...list.map((r) => r.maxInFlight));
  const inv = Math.max(...list.map((r) => r.invocations));
  console.log(`  ${envId.slice(0, 8)}  handled=${list.length}  maxInFlight=${maxIf}  invocations=${inv}  pid=${list[0].pid}`);
}
