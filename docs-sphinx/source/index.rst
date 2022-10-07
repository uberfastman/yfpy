.. toctree::
   :hidden:
   :maxdepth: 2

   index
   Quickstart <yfpy-quickstart>
   Package <_autosummary/yfpy>
   Tests <_autosummary/test>

.. swap "self" with "index" if you want to avoid a circular toctree (sacrifices having toctree entries for subsections of the index.rst included content)
   self

.. include:: ../../README.md
   :parser: myst_parser.sphinx_

.. content for separate readme_link.md if needed
   ```{include} ../../README.md
   :relative-docs: docs/
   :relative-images:
   ```
