"""Write a checksum for the verified installer built on the current runner."""

import hashlib
from pathlib import Path

from ppx_py import Settings
from ppx_py.packaging import installer_path, verify_installer


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    installer = installer_path(root, Settings.load(root / "ppx.toml"))
    errors = verify_installer(installer)
    if errors:
        raise SystemExit("安装包校验失败: " + "; ".join(errors))
    digest = hashlib.sha256()
    with installer.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    output = root / "build" / "SHA256SUMS"
    output.write_text(f"{digest.hexdigest()}  {installer.name}\n", encoding="utf-8")
    print(f"已生成: {output}")


if __name__ == "__main__":
    main()
