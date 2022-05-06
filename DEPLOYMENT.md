# YFPY Deployment

1. (Optional) Clear virtual machine of old requirements:

    ```shell
    pip uninstall -y -r <(pip freeze)
    ```

2. (Optional) Check `requirements.txt` and `requirement-dev.txt` for latest dependency versions.

3. (Optional) Update virtual machine with the latest dependencies:

    ```shell
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```
   
4. Lint code with `flake8`:

    ```shell
    flake8 . --count --show-source --statistics
    ```

5. Check code security with `bandit`:

    ```shell
    bandit -r yfpy/
    ```

6. Run *all* `pytest` tests (see following commands for running subsets of tests):

    ```shell
    python -m pytest
    ```

7. Run *all* `pytest` tests *verbosely*:

    ```shell
    python -m pytest -v -s
    ```

8. Run `pytest` unit tests:

    ```shell
    python -m pytest -v -s -m unit
    ```

9. Run `pytest` integration tests:

    ```shell
    python -m pytest -v -s -m integration
    ```

10. (Optional) Run all tests from `pytest` file:

     ```shell
     python -m pytest -v -s -m integration test/integration/test_api_game_data.py
     ```

11. (Optional) Run *specific* test from `pytest` file:

     ```shell
     python -m pytest -v -s -m integration test/integration/test_api_game_data.py -k test_get_game_key_by_season
     ```

12. Update the Sphinx documentation:

     ```shell
     cd docs-sphinx
     make html    
     ```
   
13. Check Sphinx documentation locally:

     ```shell
     open build/html/index.html
     ```
   
14. Navigate to root directory:

     ```shell
     cd ..
     ```

15. Execute `git add .`, `git commit -m 'commit message'`, and `git push`.

16. Update the git tag:

     `git tag -a [tag_name/version] -m [message]`

     ```shell
     git tag -a v1.0.0 -m 'first release'
     git push origin --tags
     ```

17. Build the package (will also auto-update the version based on teh above git tag):

     ```shell
     python setup.py sdist bdist_wheel
     ```

18. Once more execute `git add .`, `git commit -m 'commit message'`, and `git push`.

19. Install `twine` (if not already installed):

     ```shell
     pip install twine
     ```

20. Check packages before distribution:

    ```shell
    twine check dist/*
    ```

21. Deploy to Test PyPI to check:

     ```shell
     twine upload -r testpypi dist/*
     ```

22. Deploy to PyPI:

     ```shell
     twine upload dist/*
     ```
