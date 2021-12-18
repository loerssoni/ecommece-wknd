import os
from pathlib import Path

def makeparents(path):
    parent_dir = Path(path).parent
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)