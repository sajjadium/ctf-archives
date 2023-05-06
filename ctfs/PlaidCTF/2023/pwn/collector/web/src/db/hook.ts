
const MILLIS_BETWEEN_HOOKS = 1000;
const MAX_HOOK_QUEUE = 10;
const hookAt: (() => void)[] = [];
let lastHookAt = Date.now();

function triggerNextHook() {
  const trigger = hookAt.shift()!;
  lastHookAt = Date.now();
  trigger();
  if (hookAt.length > 0) setTimeout(triggerNextHook, MILLIS_BETWEEN_HOOKS);
}

export function requestHook(): Promise<'can-hook' | 'no-hook'> {
  return new Promise((resolve) => {
    if (hookAt.length >= MAX_HOOK_QUEUE) {
      resolve('no-hook');
      return;
    }

    hookAt.push(() => resolve('can-hook'));
    if (hookAt.length === 1) {
      const now = Date.now();
      setTimeout(triggerNextHook, (lastHookAt + MILLIS_BETWEEN_HOOKS) - now);
    }
  });
}