import assert from 'node:assert/strict'
import test from 'node:test'

async function loadBridge(windowValue) {
  if (windowValue === undefined) delete globalThis.window
  else globalThis.window = windowValue
  return import(`../src/index.js?test=${Math.random()}`)
}

test.afterEach(() => {
  delete globalThis.window
})

test('can be imported outside a browser and reports a stable error', async () => {
  const { ppx } = await loadBridge(undefined)
  await assert.rejects(ppx.call('system.test'), { name: 'PpxError', code: 'BRIDGE_UNAVAILABLE' })
})

test('returns RPC data and converts RPC failures', async () => {
  const requestIds = []
  const target = {
    pywebview: { api: { call: async (method, _params, requestId) => {
      requestIds.push(requestId)
      return method === 'ok'
        ? { ok: true, data: 42, requestId }
        : { ok: false, error: { code: 'DENIED', message: 'no' }, requestId }
    } } },
    addEventListener() {},
  }
  const { ppx } = await loadBridge(target)
  assert.equal(await ppx.call('ok'), 42)
  const denied = await ppx.call('fail').catch((value) => value)
  assert.equal(denied.name, 'PpxError')
  assert.equal(denied.code, 'DENIED')
  assert.equal(denied.requestId, requestIds[1])
  assert.equal(requestIds.length, 2)
  assert.ok(requestIds.every((value) => typeof value === 'string' && value.length > 5))
})

test('subscribes, dispatches and unsubscribes events', async () => {
  const target = { pywebview: { api: { call: async () => ({ ok: true }) } }, addEventListener() {} }
  const { ppx } = await loadBridge(target)
  const received = []
  const unsubscribe = ppx.on('changed', (value) => received.push(value))
  target.__ppxDispatch('changed', 1)
  assert.equal(unsubscribe(), true)
  target.__ppxDispatch('changed', 2)
  assert.deepEqual(received, [1])
})

test('times out a stalled RPC call', async () => {
  const target = {
    pywebview: { api: { call: () => new Promise(() => {}) } },
    addEventListener() {},
  }
  const { ppx } = await loadBridge(target)
  const error = await ppx.call('slow', null, { timeoutMs: 10 }).catch((value) => value)
  assert.equal(error.name, 'PpxError')
  assert.equal(error.code, 'TIMEOUT')
  assert.ok(error.requestId)
})

test('uses one timeout budget for bridge readiness and RPC', async () => {
  const originalNow = Date.now
  const originalSetTimeout = globalThis.setTimeout
  const readings = [1_000, 1_025]
  let scheduledDelay
  Date.now = () => readings.shift() ?? 1_025
  globalThis.setTimeout = (callback, delay) => {
    scheduledDelay = delay
    return originalSetTimeout(callback, 0)
  }
  const target = {
    crypto: { randomUUID: () => 'request-budget' },
    pywebview: { api: { call: () => new Promise(() => {}) } },
    addEventListener() {},
  }
  try {
    const { ppx } = await loadBridge(target)
    const error = await ppx.call('slow', null, { timeoutMs: 30 }).catch((value) => value)
    assert.equal(error.code, 'TIMEOUT')
    assert.equal(error.requestId, 'request-budget')
    assert.equal(scheduledDelay, 5)
  } finally {
    Date.now = originalNow
    globalThis.setTimeout = originalSetTimeout
  }
})

test('normalizes transport failures to a stable bridge error', async () => {
  const target = {
    pywebview: { api: { call: async () => { throw new Error('transport failed') } } },
    addEventListener() {},
  }
  const { ppx } = await loadBridge(target)
  const error = await ppx.call('broken').catch((value) => value)
  assert.equal(error.code, 'BRIDGE_ERROR')
  assert.ok(error.requestId)
})

test('rejects a ready event when the bridge is still unavailable', async () => {
  let readyListener
  const target = {
    addEventListener(_name, listener) { readyListener = listener },
  }
  const { ppx } = await loadBridge(target)
  const pending = ppx.ready({ timeoutMs: 100 })
  readyListener()
  await assert.rejects(pending, { name: 'PpxError', code: 'BRIDGE_UNAVAILABLE' })
})

test('timeoutMs zero disables the RPC deadline', async () => {
  const target = { pywebview: { api: { call: async () => ({ ok: true, data: 'downloaded' }) } } }
  const { ppx } = await loadBridge(target)
  assert.equal(await ppx.call('download', null, { timeoutMs: 0 }), 'downloaded')
})

test('readiness removes its event listener on timeout and can retry', async () => {
  const registered = new Set()
  const target = {
    addEventListener(_event, listener) { registered.add(listener) },
    removeEventListener(_event, listener) { registered.delete(listener) },
  }
  const { ppx } = await loadBridge(target)
  await assert.rejects(ppx.ready({ timeoutMs: 5 }), { code: 'TIMEOUT' })
  assert.equal(registered.size, 0)
  const waiting = ppx.ready({ timeoutMs: 100 })
  target.pywebview = { api: { call() {} } }
  for (const listener of registered) listener()
  await waiting
  assert.equal(registered.size, 0)
})

test('one failing event subscriber does not block other subscribers', async () => {
  const target = {}
  const { ppx } = await loadBridge(target)
  const errors = []
  const originalError = console.error
  console.error = (...args) => errors.push(args)
  try {
    const received = []
    ppx.on('progress', () => { throw new Error('broken component') })
    ppx.on('progress', async () => { throw new Error('broken async component') })
    ppx.on('progress', value => received.push(value))
    target.__ppxDispatch('progress', 42)
    await Promise.resolve()
    assert.deepEqual(received, [42])
    assert.equal(errors.length, 2)
  } finally {
    console.error = originalError
  }
})

test('repeated unsubscribe cannot remove a newer subscription', async () => {
  const target = {}
  const { ppx } = await loadBridge(target)
  const stop = ppx.on('event', () => {})
  assert.equal(stop(), true)
  const received = []
  ppx.on('event', value => received.push(value))
  assert.equal(stop(), false)
  target.__ppxDispatch('event', 1)
  assert.deepEqual(received, [1])
})
