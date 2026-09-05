import tempfile
import unittest
from pathlib import Path

from PIL import Image

from ppx_py.commands.icon import IconError, generate_icons


class IconTests(unittest.TestCase):
    def test_generates_png_ico_and_icns_from_one_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "master.png"
            Image.new("RGBA", (1024, 1024), (20, 100, 220, 200)).save(source)
            generated = generate_icons(source, root / "assets")
            self.assertEqual([path.name for path in generated], ["logo.png", "logo.ico", "logo.icns"])
            with Image.open(root / "assets/logo.png") as image:
                self.assertEqual(image.size, (1024, 1024))
                self.assertEqual(image.format, "PNG")
            with Image.open(root / "assets/logo.ico") as image:
                self.assertEqual(image.format, "ICO")
                self.assertIn((256, 256), image.ico.sizes())
            with Image.open(root / "assets/logo.icns") as image:
                self.assertEqual(image.format, "ICNS")

    def test_rejects_small_or_non_square_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, size in (("small.png", (256, 256)), ("wide.png", (1024, 512))):
                source = root / name
                Image.new("RGB", size, "red").save(source)
                with self.subTest(size=size), self.assertRaises(IconError):
                    generate_icons(source, root / "assets")


if __name__ == "__main__":
    unittest.main()
