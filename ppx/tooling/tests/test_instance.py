import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ppx_py.instance import InstanceAlreadyRunning, InstanceLock


class InstanceTests(unittest.TestCase):
    def test_crashed_process_releases_lock_without_deleting_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'instance.lock'
            script = (
                'import sys\nfrom pathlib import Path\n'
                'from ppx_py.instance import InstanceLock\n'
                'lock = InstanceLock(Path(sys.argv[1]))\n'
                'lock.acquire()\nprint("locked", flush=True)\n'
                'sys.stdin.read()\n'
            )
            process = subprocess.Popen(
                [sys.executable, '-c', script, str(path)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True,
            )
            try:
                self.assertEqual(process.stdout.readline().strip(), 'locked')
                with self.assertRaises(InstanceAlreadyRunning):
                    InstanceLock(path).acquire()
                process.kill()
                process.communicate(timeout=10)
                with InstanceLock(path):
                    self.assertTrue(path.is_file())
                    with self.assertRaises(InstanceAlreadyRunning):
                        InstanceLock(path).acquire()
                with InstanceLock(path):
                    pass
            finally:
                if process.poll() is None:
                    process.kill()
                process.communicate(timeout=10)


if __name__ == '__main__':
    unittest.main()
