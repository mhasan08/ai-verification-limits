import os
import shutil

# Folders to remove
DIRS_TO_REMOVE = [
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ipynb_checkpoints",
]

# File extensions to remove
FILE_EXTENSIONS = [
    ".pyc",
    ".pyo",
    ".pyd",
    ".log",
    ".tmp",
]

def remove_dirs(root):
    for dirpath, dirnames, _ in os.walk(root):
        for d in list(dirnames):
            if d in DIRS_TO_REMOVE:
                full_path = os.path.join(dirpath, d)
                print(f"Removing directory: {full_path}")
                shutil.rmtree(full_path, ignore_errors=True)

def remove_files(root):
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if any(f.endswith(ext) for ext in FILE_EXTENSIONS):
                full_path = os.path.join(dirpath, f)
                print(f"Removing file: {full_path}")
                try:
                    os.remove(full_path)
                except Exception as e:
                    print(f"Failed to remove {full_path}: {e}")

def main():
    root = os.path.abspath(".")
    print(f"Cleaning project at: {root}\n")

    remove_dirs(root)
    remove_files(root)

    print("\nCleanup complete.")

if __name__ == "__main__":
    main()