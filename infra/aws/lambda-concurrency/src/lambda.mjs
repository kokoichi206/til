import { work } from './shared.mjs';

const SLEEP_MS = Number(process.env.SLEEP_MS ?? 5000);

// Plain Lambda handler behind a Function URL (payload format 2.0).
export const handler = async () => {
  const result = await work(SLEEP_MS);
  return {
    statusCode: 200,
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ runner: 'lambda-plain', ...result }),
  };
};
