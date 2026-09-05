"""Generate the platform icon set from one developer-owned source image."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import List, Optional

from PIL import Image, UnidentifiedImageError

from ..project import find_project_root, load_settings


class IconError(RuntimeError):
    pass


def generate_icons(source: Path, output: Path) -> List[Path]:
    source = source.expanduser().resolve()
    output = output.expanduser().resolve()
    if not source.is_file():
        raise IconError(f"找不到图标源文件: {source}")
    try:
        with Image.open(source) as opened:
            opened.load()
            if opened.width != opened.height:
                raise IconError(f"图标必须是正方形，当前为 {opened.width}×{opened.height}")
            if opened.width < 512:
                raise IconError(f"图标至少需要 512×512，当前为 {opened.width}×{opened.height}")
            image = opened.convert("RGBA")
    except IconError:
        raise
    except (OSError, UnidentifiedImageError) as exc:
        raise IconError(f"无法读取图标图片: {exc}") from exc

    output.mkdir(parents=True, exist_ok=True)
    names = ("logo.png", "logo.ico", "logo.icns")
    with tempfile.TemporaryDirectory(prefix=".ppx-icons-", dir=output) as directory:
        temporary = Path(directory)
        master = image.resize((1024, 1024), Image.Resampling.LANCZOS)
        master.save(temporary / "logo.png", format="PNG", optimize=True)
        master.save(
            temporary / "logo.ico",
            format="ICO",
            sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
        )
        master.save(temporary / "logo.icns", format="ICNS")
        for name in names:
            if not (temporary / name).is_file() or (temporary / name).stat().st_size == 0:
                raise IconError(f"生成图标失败: {name}")
        for name in names:
            os.replace(temporary / name, output / name)
    return [output / name for name in names]


def run(args: object) -> int:
    try:
        source = Path(str(getattr(args, "source")))
        configured_output: Optional[str] = getattr(args, "output", None)
        if configured_output:
            output = Path(configured_output)
        else:
            root = find_project_root()
            output = load_settings(root).asset_dir
        generated = generate_icons(source, output)
        print("三端图标已生成：")
        for path in generated:
            print(f"  {path}")
        return 0
    except Exception as exc:
        print(f"[失败] {exc}")
        return 1
