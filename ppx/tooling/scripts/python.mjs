import { existsSync } from 'node:fs'
import { resolve } from 'node:path'
import { spawnSync } from 'node:child_process'

const root = resolve(import.meta.dirname, '../../..')
const localPython = process.platform === 'win32'
  ? resolve(root, '.venv/Scripts/python.exe')
  : resolve(root, '.venv/bin/python')
const executable = process.env.PPX_PYTHON || (existsSync(localPython)
  ? localPython
  : process.platform === 'win32' ? 'python' : 'python3')
const result = spawnSync(executable, process.argv.slice(2), {
  cwd: root,
  env: { ...process.env, PYTHONUTF8: process.env.PYTHONUTF8 ?? '1' },
  stdio: 'inherit'
})
if (result.error) {
  console.error(result.error.message)
  process.exit(1)
}
process.exit(result.status ?? 1)
