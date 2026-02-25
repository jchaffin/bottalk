#!/usr/bin/env node

const { spawn } = require("node:child_process");

function hasLocalFlag() {
  // Check direct args, npm config, and npm lifecycle script detection
  return (
    process.argv.includes("--local") ||
    process.env.npm_config_local != null ||
    process.env.npm_lifecycle_script?.includes("--local")
  );
}

function run(command, args, env = process.env) {
  return new Promise((resolve) => {
    const child = spawn(command, args, { stdio: "inherit", env });
    child.on("exit", (code) => resolve(code ?? 1));
  });
}

async function main() {
  const local = hasLocalFlag();
  const env = { ...process.env };

  if (local) {
    env.PCC_AGENT_NAME = "bottalk-agent-local";
    env.NEXT_PUBLIC_PCC_AGENT_NAME = "bottalk-agent-local";
    console.log("[dev] local mode enabled -> bottalk-agent-local");
  }

  const killCode = await run("npm", ["run", "kill-ports"], env);
  if (killCode !== 0) process.exit(killCode);

  const devCode = await run("npm", ["run", "dev:frontend"], env);
  process.exit(devCode);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

