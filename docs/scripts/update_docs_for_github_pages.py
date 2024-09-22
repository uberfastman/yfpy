from pathlib import Path
import shutil

base_project_dir = Path(__file__).parent.parent.parent
docs_dir = base_project_dir / "docs"

print("Copying CNAME file to \"/docs\" for GitHub Pages...")

cname_file_path = base_project_dir / "resources" / "documentation" / "CNAME"
shutil.copyfile(cname_file_path, docs_dir / "CNAME")

print("...successfully prepared docs for GitHub Pages.")
