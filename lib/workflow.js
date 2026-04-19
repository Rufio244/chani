export async function runWorkflow(step, context) {

  const flow = {
    analyze: "ai",
    decide: "orchestrator",
    execute: "worker",
    store: "memory"
  };

  const next = flow[step];

  return {
    current: step,
    next,
    context
  };
}
