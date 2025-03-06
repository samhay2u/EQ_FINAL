from pathlib import Path
from typing import Optional, Set, List


class ProjectTreePrinter:
    def __init__(
            self,
            root_path: str,
            show_source_for: List[str],
            ignore_patterns: Optional[Set[str]] = None,
            skip_source_for: Optional[List[str]] = None
    ):
        self.root_path = Path(root_path)
        self.ignore_patterns = ignore_patterns or set()
        self.show_source_for = show_source_for
        self.skip_source_for = skip_source_for or []
        self.files_to_show_source = []

    def print_tree(self) -> None:
        """Print the project tree in the specified format with source code documentation."""
        if not self.root_path.exists():
            print(f"Error: Path '{self.root_path}' does not exist")
            return

        # Print header
        print("# EQ_FINAL_03_04 - Project Solution Tree")
        print("# Automated ETL Pipeline for Earthquake Submission Data Processing")
        print("#" * 80)
        print("#")
        print("#")
        print("# Project Solution Tree:")
        print("# ====================")
        print(f"# {self.root_path.name}/")

        # Print directory structure
        self._print_directory(self.root_path, "# │   ", 0)

        # Print source code section
        print("#")
        print("# Source Code Documentation:")
        print("# " + "=" * 80)
        self._print_source_code()

    def _print_directory(self, directory: Path, prefix: str, depth: int) -> None:
        """Print directory structure with specific formatting."""
        try:
            entries = sorted(
                [entry for entry in directory.iterdir() if not self._should_ignore(entry)],
                key=lambda x: (x.is_file(), x.name.lower())
            )
        except PermissionError:
            print(f"{prefix}└── Error: Permission denied")
            return

        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            print(f"{prefix}{connector}{entry.name}")

            if entry.is_file() and self._should_show_source(entry) and not self._should_skip_source(entry):
                self.files_to_show_source.append(entry)

            if entry.is_dir():
                new_prefix = prefix + ("    " if is_last else "│   ")
                self._print_directory(entry, new_prefix, depth + 1)

    def _should_show_source(self, path: Path) -> bool:
        """Check if file's source code should be displayed."""
        return (path.name in self.show_source_for or
                (path.name == '__init__.py' and '__init__.py' in self.show_source_for))

    def _should_skip_source(self, path: Path) -> bool:
        """Check if file's source code should be skipped even if in show_source_for."""
        return path.name in self.skip_source_for

    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored."""
        # Ignore patterns check
        if any(pattern in str(path) for pattern in self.ignore_patterns):
            return True

        # Handle tmp files/directories
        if path.name.startswith('tmp') and any(char.isdigit() or char in '_-' for char in path.name[3:]):
            return True

        # Show only top-level .hypothesis directory
        if '.hypothesis' in str(path):
            parts = path.parts
            if len(parts) > parts.index('.hypothesis') + 1:
                if 'tmp' in parts or 'unicode_data' in parts:
                    return True

        return False

    def _print_source_code(self) -> None:
        """Print source code for specified files with banner separators."""
        for file_path in self.files_to_show_source:
            # Print banner header
            print("#" + "#" * 96)
            print(f"# {file_path.name} - Python Source File")
            print(f"# {file_path.absolute()}")
            print("#" + "#" * 96)

            try:
                with file_path.open('r', encoding='utf-8') as f:
                    for line in f:
                        print(f"# {line.rstrip()}")
            except Exception as e:
                print(f"# Error reading file: {e}")
            print("#")


if __name__ == "__main__":
    # Updated path with the space before EQ_FINAL_03_04
    project_path = r"C:\Users\samha\PycharmProjects\ EQ_FINAL_03_04"

    # Try alternative method to get the current directory if the above path doesn't work
    import os

    current_script_dir = os.path.dirname(os.path.abspath(__file__))

    # Print both paths for debugging
    print(f"Attempting to access directory (specified path): {project_path}")
    print(f"Current script directory: {current_script_dir}")

    # Try both paths
    paths_to_try = [
        project_path,
        current_script_dir,
        os.path.dirname(current_script_dir)  # Parent directory
    ]

    # Find the first path that exists
    for path in paths_to_try:
        if os.path.exists(path):
            print(f"Found valid path: {path}")
            project_path = path
            break

    files_to_show = [
        'main_consolidated.py',
        'io_analyzer.py',
        'etl_test_gen_runner.py',
        'consolidated_config.json',
        'collection_n_schema.json',
        'collection_n_schema.xml',
        'collection_b_schema.json'
    ]

    # Files to skip showing source code for
    skip_source_files = [
        'main_consolidated.py'  # Skip showing source for this file
    ]

    ignore_patterns = {
        '__pycache__',
        '.git',
        '.idea',
        'venv',
        '.pytest_cache',
        '.hypothesis'
    }

    printer = ProjectTreePrinter(
        root_path=project_path,
        show_source_for=files_to_show,
        ignore_patterns=ignore_patterns,
        skip_source_for=skip_source_files
    )
    printer.print_tree()