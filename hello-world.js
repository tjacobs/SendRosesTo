require('dotenv').config();
const { Agent, run } = require('@openai/agents');

const agent = new Agent({
  name: 'Assistant',
  instructions: 'You are a helpful assistant',
});

async function main() {
  const result = await run(
    agent,
    'Buy the best dark chocolate online.',
  );
  console.log(result.finalOutput);
}

main().catch(console.error);