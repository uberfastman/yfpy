# YFPY Deployment

1. *(Optional)* Clear virtual machine of old requirements:

    ```shell
    pip uninstall -y -r <(pip freeze)
    ```

2. *(Optional)* Check `requirements.txt` and `requirement-dev.txt` for latest dependency versions.

3. *(Optional)* Update virtual machine with the latest dependencies:

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

10. *(Optional)* Run all tests from `pytest` file:

    ```shell
    python -m pytest -v -s -m integration test/integration/test_api_game_data.py
    ```

11. *(Optional)* Run *specific* test from `pytest` file:

    ```shell
    python -m pytest -v -s -m integration test/integration/test_api_game_data.py -k test_get_game_key_by_season
    ```

12. Update the git tag:

    `git tag -a [tag_name/version] -m [message]`

    ```shell
    git tag -a v1.0.0 -m 'first release'
    git push origin --tags
    ```

13. *(Optional)* Build the documentation and PyPI package independent of deployment:

    ```shell
    make -C docs-sphinx docs
    ```
    
    ***Note***: You can run `make -C docs-sphinx docs_no_build` to recreate documentation without building the PyPI package with `setup.py`.

14. *(Optional)* Check Sphinx documentation locally:

    ```shell
    make -C docs-sphinx open_local_docs
    ```
    
15. Install `twine` (if not already installed):

    ```shell
    pip install twine
    ```
    
16. *(Optional)* Test deployment by building the PyPI packages, recreating the documentation, and deploying to Test PyPI:

    ```shell
    make -C docs-sphinx test_deploy
    ```

17. Deploy YFPY by building the PyPI packages, recreating the Sphinx documentation, and deploying to PyPI:

    ```shell
    make -C docs-sphinx deploy
    ```

18. Update YFPY GitHub repository:

    ```shell
    git add .
    git commit -m 'commit message'
    git push
    ```
