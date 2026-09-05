import { rmSync } from 'node:fs'
import { resolve } from 'node:path'

const projectRoot = resolve(import.meta.dirname, '../../..')
// dist/release contains maintainer-built package artifacts and must survive app cleanup.
for (const relative of ['build', 'gui/dist', 'gui/node_modules']) {
  rmSync(resolve(projectRoot, relative), { recursive: true, force: true })
}
