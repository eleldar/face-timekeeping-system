import os
import sys
from pathlib import Path

root_dir = Path("tests/datasets")
e1p1 = root_dir / "employee1photo1.jpg"
e1p2 = root_dir / "employee1photo2.jpg"
e2p1 = root_dir / "employee2photo1.jpg"
e1fake = root_dir / "employee1fake.jpg"
e3unk = root_dir / "employee3unknown.jpg"

src_dir = Path("src")
sys.path.append(str(src_dir.resolve()))
