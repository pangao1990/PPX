"""Create the intentionally small developer-facing PPX project."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import uuid
from importlib.resources import files
from pathlib import Path
from typing import Optional

from .project import find_project_root


SUPPORTED_FRONTENDS = ("vanilla", "vue", "react")


def _slug(name: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not value:
        raise ValueError("项目名称至少要包含一个英文字母或数字")
    return value


def create_project(name: str, directory: Optional[str] = None, frontend: str = "vanilla") -> Path:
    if frontend not in SUPPORTED_FRONTENDS:
        raise ValueError(f"不支持的前端模板 {frontend}，可选值: {', '.join(SUPPORTED_FRONTENDS)}")
    slug = _slug(name)
    target = (Path(directory).resolve() if directory else (Path.cwd() / slug).resolve())
    if target.exists() and any(target.iterdir()):
        raise FileExistsError(f"目标目录不是空目录: {target}")
    target.mkdir(parents=True, exist_ok=True)
    for relative in ("api/resources", "gui/src", "ppx/assets"):
        (target / relative).mkdir(parents=True, exist_ok=True)

    files_to_write = {
        "api/__init__.py": "\"\"\"Application business APIs.\"\"\"\n",
        "api/api.py": (
            "from ppx_py import api_method\n\n\n"
            "@api_method(\"user.greet\")\n"
            "def greet(name: str = \"PPX\") -> dict[str, str]:\n"
            "    return {\"message\": f\"你好，{name}！\"}\n"
        ),
        "api/requirements.txt": "# 在这里填写业务层额外的 Python 依赖。\n",
        "package.json": json.dumps({
            "name": slug, "private": True, "version": "0.1.0", "packageManager": "pnpm@11.25.0",
            "engines": {"node": ">=22.13.0", "pnpm": ">=11.0.0 <12.0.0"},
            "scripts": {"dev": "ppx dev", "doctor": "ppx doctor", "update": "ppx update", "build": "ppx build"},
        }, ensure_ascii=False, indent=2) + "\n",
        "pnpm-workspace.yaml": (
            "packages:\n  - gui\n\n"
            "allowBuilds:\n  esbuild: true\n\n"
            "overrides:\n  postcss: 8.5.26\n"
        ),
        "ppx.toml": _config(name, slug),
        "ppx.lock": _lock(),
        ".gitignore": ".venv/\nnode_modules/\ngui/node_modules/\ngui/dist/\nbuild/\n*.py[cod]\n__pycache__/\n",
    }
    files_to_write.update(_frontend_files(slug, frontend))
    for relative, content in files_to_write.items():
        (target / relative).write_text(content, encoding="utf-8")
    assets = files("ppx_py").joinpath("template/assets")
    for name_in_package in ("logo.png", "logo.ico", "logo.icns", "dmg-background.png"):
        with assets.joinpath(name_in_package).open("rb") as source:
            (target / "ppx/assets" / name_in_package).write_bytes(source.read())
    return target


def _frontend_files(slug: str, frontend: str) -> dict[str, str]:
    common = {
        "gui/src/style.css": (
            "body{font-family:system-ui;margin:0;display:grid;place-items:center;min-height:100vh}"
            "main,#app{max-width:680px;padding:32px;text-align:center}"
            "body{background:#f2f7f4;color:#26463a}button{padding:.7rem 1rem;border:0;"
            "border-radius:8px;background:#17785f;color:white;cursor:pointer}"
            "button:disabled{opacity:.5;cursor:wait}p{line-height:1.8;overflow-wrap:anywhere}\n"
        ),
    }
    dependencies = {"ppx-js": "6.0.0"}
    development = {"vite": "8.2.2"}
    entry = "main.js"

    if frontend == "vanilla":
        common["gui/src/main.js"] = (
            "import { ppx } from 'ppx-js'\n"
            "import './style.css'\n\n"
            "const app = document.querySelector('#app')\n"
            "app.innerHTML = '<h1>PPX</h1><button>调用 Python</button><p role=\"status\">请在 ppx dev 打开的桌面窗口中体验。</p>'\n"
            "app.querySelector('button').addEventListener('click', async () => {\n"
            "  const button = app.querySelector('button')\n"
            "  button.disabled = true\n"
            "  try {\n"
            "    const result = await ppx.call('user.greet', { name: '开发者' })\n"
            "    app.querySelector('p').textContent = result.message\n"
            "  } catch (error) {\n"
            "    app.querySelector('p').textContent = `${error.code}: ${error.message}`\n"
            "  } finally {\n"
            "    button.disabled = false\n"
            "  }\n"
            "})\n"
        )
    elif frontend == "vue":
        dependencies["vue"] = "3.5.42"
        development["@vitejs/plugin-vue"] = "6.0.8"
        common["gui/vite.config.js"] = (
            "import { defineConfig } from 'vite'\n"
            "import vue from '@vitejs/plugin-vue'\n\n"
            "export default defineConfig({ plugins: [vue()] })\n"
        )
        common["gui/src/main.js"] = (
            "import { createApp } from 'vue'\n"
            "import App from './App.vue'\n"
            "import './style.css'\n\n"
            "createApp(App).mount('#app')\n"
        )
        common["gui/src/App.vue"] = '''<script setup>
import { ref } from 'vue'
import { ppx } from 'ppx-js'

const message = ref('请在 ppx dev 打开的桌面窗口中体验。')
const busy = ref(false)
async function greet() {
  if (busy.value) return
  busy.value = true
  try {
    const result = await ppx.call('user.greet', { name: 'Vue 开发者' })
    message.value = result.message
  } catch (error) {
    message.value = `${error.code}: ${error.message}`
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <main><h1>PPX + Vue</h1><button :disabled="busy" @click="greet">{{ busy ? "调用中…" : "调用 Python" }}</button><p role="status">{{ message }}</p></main>
</template>
'''
    else:
        entry = "main.jsx"
        dependencies.update({"react": "19.2.8", "react-dom": "19.2.8"})
        development["@vitejs/plugin-react"] = "6.1.1"
        common["gui/vite.config.js"] = (
            "import { defineConfig } from 'vite'\n"
            "import react from '@vitejs/plugin-react'\n\n"
            "export default defineConfig({ plugins: [react()] })\n"
        )
        common["gui/src/main.jsx"] = (
            "import { StrictMode } from 'react'\n"
            "import { createRoot } from 'react-dom/client'\n"
            "import App from './App.jsx'\n"
            "import './style.css'\n\n"
            "createRoot(document.querySelector('#app')).render(<StrictMode><App /></StrictMode>)\n"
        )
        common["gui/src/App.jsx"] = '''import { useState } from 'react'
import { ppx } from 'ppx-js'

export default function App() {
  const [message, setMessage] = useState('请在 ppx dev 打开的桌面窗口中体验。')
  const [busy, setBusy] = useState(false)
  async function greet() {
    if (busy) return
    setBusy(true)
    try {
      const result = await ppx.call('user.greet', { name: 'React 开发者' })
      setMessage(result.message)
    } catch (error) {
      setMessage(`${error.code}: ${error.message}`)
    } finally {
      setBusy(false)
    }
  }
  return <main><h1>PPX + React</h1><button disabled={busy} onClick={greet}>{busy ? "调用中…" : "调用 Python"}</button><p role="status">{message}</p></main>
}
'''

    common["gui/index.html"] = (
        '<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"><title>PPX</title>'
        f'</head><body><div id="app"></div><script type="module" src="/src/{entry}"></script></body></html>\n'
    )
    common["gui/package.json"] = json.dumps({
        "name": f"{slug}-gui",
        "private": True,
        "type": "module",
        "version": "0.1.0",
        "scripts": {"dev": "vite", "build": "vite build"},
        "dependencies": dependencies,
        "devDependencies": development,
    }, ensure_ascii=False, indent=2) + "\n"
    return common


def initialize_project(root: Optional[Path] = None) -> int:
    project_root = root or find_project_root()
    requirements = project_root / "api" / "requirements.txt"
    if requirements.is_file() and any(
        line.strip() and not line.lstrip().startswith("#")
        for line in requirements.read_text(encoding="utf-8").splitlines()
    ):
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements)],
            cwd=project_root,
            check=False,
        )
        if result.returncode:
            return result.returncode
    result = subprocess.run(["pnpm", "install"], cwd=project_root, check=False)
    if result.returncode:
        return result.returncode
    from .commands.doctor import run
    return run(object())


def _config(name: str, slug: str) -> str:
    return f'''[project]
name = {json.dumps(name, ensure_ascii=False)}
slug = "{slug}"
version = "0.1.0"
identifier = "com.example"
developer = "Your Name"
description = "A PPX desktop application"
website = "https://example.com"
windowsAppId = "{str(uuid.uuid4()).upper()}"
format = 6

[python]
modules = ["api.api"]

[paths]
frontend = "gui"
resources = "api/resources"
assets = "ppx/assets"

[window]
widthRatio = 0.6667
heightRatio = 0.8
minWidthRatio = 0.5
minHeightRatio = 0.5
resizable = true
fullscreen = false
alwaysOnTop = false
confirmClose = false
backgroundColor = "#FFFFFF"

[development]
port = 5173

[storage]
filename = "storage.json"

[applicationUpdate]
enabled = false
releaseUrl = ""

[compatibility]
pythonApi = "6.0"
javascriptApi = "6.0"
dataSchema = "1"

[framework]
python = "6.0.0"
javascript = "6.0.0"
channel = "stable"
releaseUrl = "https://api.github.com/repos/pangao1990/PPX/releases/latest"
'''


def _lock() -> str:
    return '''# 此文件由 ppx update 管理，请勿手动修改。
lockVersion = 1
projectFormat = 6

[framework]
python = "6.0.0"
javascript = "6.0.0"

[compatibility]
pythonApi = "6.0"
javascriptApi = "6.0"
dataSchema = "1"
'''
