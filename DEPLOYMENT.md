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

12. *(Optional)* Build the documentation and PyPI package independent of deployment:

    ```shell
    make -C docs-sphinx docs
    ```
    
    ***Note***: You can run `make -C docs-sphinx docs_no_build` to recreate documentation without building the PyPI package with `setup.py`.

13. *(Optional)* Check Sphinx documentation locally:

    ```shell
    make -C docs-sphinx open_local_docs
    ```

14. Create a git commit:

    ```shell
    git add .
    git commit -m 'commit message'
    ```

15. Update the git tag with the new version:

    `git tag -a [tag_name/version] -m [message]`

    ```shell
    git tag -a v1.0.0 -m 'release message'
    git push origin --tags
    ```
    
16. Install `twine` (if not already installed):

    ```shell
    pip install twine
    ```
    
17. *(Optional)* Test deployment by building the PyPI packages, recreating the documentation, and deploying to Test PyPI:

    ```shell
    make -C docs-sphinx test_deploy
    ```

18. Deploy YFPY by building the PyPI packages, recreating the Sphinx documentation, and deploying to PyPI:

    ```shell
    make -C docs-sphinx deploy
    ```

19. Build Docker container:
    ```shell
    docker compose -f compose.yaml -f compose.build.yaml build
    ```

20. *(If needed)* Authenticate with GitHub Personal Access Token (PAT):
    ```shell
    jq -r .github_personal_access_token.value auth/github/private.json | docker login ghcr.io -u uberfastman --password-stdin
    ```

21. Deploy the newly-built Docker image with respective major, minor, and patch version numbers to the GitHub Container Registry:
    ```shell
    docker push ghcr.io/uberfastman/yfpy:X.X.X
    ```

22. Create a second git commit with updated version number and documentation:

    ```shell
    git add .
    git commit -m 'update version number and docs'
    ```

23. Update YFPY GitHub repository:

    ```shell
    git push
    ```
