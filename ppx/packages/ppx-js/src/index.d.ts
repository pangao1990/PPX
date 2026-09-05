export interface PpxCallOptions {
  /** Total maximum time for bridge readiness and the RPC result. Set to 0 to disable. */
  timeoutMs?: number
}

export interface PpxRpcError {
  code?: string
  message?: string
}

export class PpxError extends Error {
  readonly code: string
  readonly requestId?: string
  constructor(error?: PpxRpcError, requestId?: string)
}

export interface PpxBridge {
  call<T = unknown>(method: string, params?: unknown, options?: PpxCallOptions): Promise<T>
  on<T = unknown>(event: string, listener: (data: T) => void): () => boolean
  ready(options?: PpxCallOptions): Promise<void>
}

export const ppx: Readonly<PpxBridge>
export default ppx
