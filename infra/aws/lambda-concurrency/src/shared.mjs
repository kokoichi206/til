import { randomUUID } from 'node:crypto';

// One id per execution environment / OS process. Assigned once at module init
// (cold start for Lambda, process start locally) and reused across warm
// invocations, so distinct envId values equal distinct execution environments.
export const ENV_ID = randomUUID();

// Module-scope counters survive across invocations while the environment is warm.
// inFlight is the number of requests currently inside work() at the same time.
let inFlight = 0;
let maxInFlight = 0;
let invocations = 0;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Simulates an I/O-bound request: increment the concurrency gauge, await, decrement.
// A runtime that multiplexes requests during the await (a normal HTTP server) will
// observe inFlight > 1; one that serializes per environment (Lambda) stays at 1.
export async function work(sleepMs) {
  invocations += 1;
  inFlight += 1;
  if (inFlight > maxInFlight) maxInFlight = inFlight;
  const inFlightAtEntry = inFlight;
  const startedAt = Date.now();
  try {
    await sleep(sleepMs);
    return {
      envId: ENV_ID,
      pid: process.pid,
      inFlightAtEntry,
      maxInFlight,
      invocations,
      durationMs: Date.now() - startedAt,
    };
  } finally {
    inFlight -= 1;
  }
}
