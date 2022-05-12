from pathlib import Path
import shutil

base_project_dir = Path(__file__).parent.parent.parent
docs_dir = base_project_dir / "docs"
docs_index_html = docs_dir / "index.html"

if docs_index_html.exists():
    print("Removing stale \"sphinx docs\" content before copying new docs...")
    shutil.rmtree(docs_dir)

print("Copying new \"sphinx docs\" to \"/docs\" for Github Pages...")

sphinx_docs_path = base_project_dir / "docs-sphinx" / "build" / "html"
shutil.copytree(sphinx_docs_path, docs_dir)

cname_file_path = base_project_dir / "resources" / "documentation" / "CNAME"
shutil.copyfile(cname_file_path, docs_dir / "CNAME")

theme_file_path = base_project_dir / "resources" / "documentation" / ".nojekyll"
shutil.copyfile(theme_file_path, docs_dir / ".nojekyll")

print("...successfully copied new \"sphinx docs\" to \"/docs\" for Github Pages.")
