const listeners = new Map()
const DEFAULT_TIMEOUT_MS = 30_000

export class PpxError extends Error {
  constructor(error, requestId) {
    super(error?.message || 'PPX API 调用失败')
    this.name = 'PpxError'
    this.code = error?.code || 'UNKNOWN'
    this.requestId = requestId
  }
}

function browserWindow() {
  if (typeof window === 'undefined') {
    throw new PpxError({ code: 'BRIDGE_UNAVAILABLE', message: 'PPX Bridge 只能在 pywebview 页面中调用' })
  }
  return window
}

function withTimeout(promise, timeoutMs, message, requestId) {
  if (!Number.isFinite(timeoutMs) || timeoutMs <= 0) return promise
  let timer
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new PpxError({ code: 'TIMEOUT', message }, requestId)), timeoutMs)
  })
  return Promise.race([promise, timeout]).finally(() => clearTimeout(timer))
}

function createRequestId(target) {
  if (typeof target.crypto?.randomUUID === 'function') return target.crypto.randomUUID()
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`
}

function ready(options = {}) {
  let target
  try {
    target = browserWindow()
  } catch (error) {
    return Promise.reject(error)
  }
  if (target.pywebview?.api?.call) return Promise.resolve()
  const timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS
  let listener
  const pending = new Promise((resolve) => {
    listener = resolve
    target.addEventListener('pywebviewready', listener, { once: true })
  })
  return withTimeout(pending, timeoutMs, `等待 PPX Bridge 就绪超时（${timeoutMs}ms）`).finally(() => {
    target.removeEventListener?.('pywebviewready', listener)
  }).then(() => {
    if (!target.pywebview?.api?.call) {
      throw new PpxError({ code: 'BRIDGE_UNAVAILABLE', message: 'pywebview 已就绪，但 PPX Bridge 不可用' })
    }
  })
}

async function call(method, params = null, options = {}) {
  const timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS
  const target = browserWindow()
  const requestId = createRequestId(target)
  const startedAt = Date.now()
  try {
    await ready({ timeoutMs })
  } catch (error) {
    if (error instanceof PpxError && !error.requestId) error.requestId = requestId
    throw error
  }
  const remainingMs = Number.isFinite(timeoutMs) && timeoutMs > 0
    ? timeoutMs - (Date.now() - startedAt)
    : timeoutMs
  if (Number.isFinite(timeoutMs) && timeoutMs > 0 && remainingMs <= 0) {
    throw new PpxError({ code: 'TIMEOUT', message: `PPX API 调用超时（${timeoutMs}ms）` }, requestId)
  }
  let result
  try {
    result = await withTimeout(
      Promise.resolve(target.pywebview.api.call(method, params, requestId)),
      remainingMs,
      `PPX API 调用超时（${timeoutMs}ms）`,
      requestId,
    )
  } catch (error) {
    if (error instanceof PpxError) throw error
    throw new PpxError(
      { code: 'BRIDGE_ERROR', message: error?.message || 'PPX Bridge 调用失败' },
      requestId,
    )
  }
  if (!result?.ok) throw new PpxError(result?.error, result?.requestId || requestId)
  return result.data
}

function on(event, listener) {
  const callbacks = listeners.get(event) || new Set()
  callbacks.add(listener)
  listeners.set(event, callbacks)
  return () => {
    const deleted = callbacks.delete(listener)
    if (!callbacks.size && listeners.get(event) === callbacks) listeners.delete(event)
    return deleted
  }
}

if (typeof window !== 'undefined') {
  window.__ppxDispatch = (event, data) => {
    for (const listener of [...(listeners.get(event) || [])]) {
      try {
        Promise.resolve(listener(data)).catch((error) => console.error('PPX 事件处理失败:', event, error))
      } catch (error) {
        console.error('PPX 事件处理失败:', event, error)
      }
    }
  }
}

export const ppx = Object.freeze({ call, on, ready })
export default ppx
