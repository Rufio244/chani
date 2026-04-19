const listeners = {};

export function emit(event, data) {
  if (listeners[event]) {
    listeners[event].forEach(fn => fn(data));
  }
}

export function on(event, fn) {
  if (!listeners[event]) listeners[event] = [];
  listeners[event].push(fn);
}
