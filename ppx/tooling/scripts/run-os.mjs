import { spawnSync } from 'node:child_process'

const platformNames = {
  darwin: 'macos',
  linux: 'linux',
  win32: 'windows'
}

const baseScript = process.argv[2]
const platformName = platformNames[process.platform]

if (!baseScript || !platformName) {
  console.error(`不支持的脚本或操作系统: ${baseScript || '(empty)'} / ${process.platform}`)
  process.exit(1)
}

const targetScript = `${baseScript}:${platformName}`
const pnpmCommand = process.platform === 'win32' ? 'pnpm.cmd' : 'pnpm'
const result = spawnSync(pnpmCommand, ['run', targetScript], {
  env: process.env,
  stdio: 'inherit'
})

if (result.error) {
  console.error(result.error.message)
  process.exit(1)
}

process.exit(result.status ?? 1)
