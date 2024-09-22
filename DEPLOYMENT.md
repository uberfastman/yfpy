# YFPY Deployment

1. *(Optional)* Clear virtual machine of old requirements:

    ```shell
    pip uninstall -y -r <(pip freeze)
    ```

2. *(Optional)* Check `requirements.txt` and `requirement-dev.txt` for latest dependency versions.

3. *(Optional)* Update virtual machine with the latest dependencies:

    ```shell
    pip install -r requirements.txt -r requirements-dev.txt
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

8. Run `pytest` integration tests:

    ```shell
    python -m pytest -v -s -m integration
    ```

9. *(Optional)* Run all tests from `pytest` file:

   ```shell
   python -m pytest -v -s -m integration test/integration/test_api_game_data.py
   ```

10. *(Optional)* Run *specific* test from `pytest` file:

    ```shell
    python -m pytest -v -s -m integration test/integration/test_api_game_data.py -k test_get_game_key_by_season
    ```

11. *(Optional)* Test Python support using [act](https://github.com/nektos/act) for GitHub Actions:

    ```shell
    act_amd -j build
    ```
    
    ***Note***: If `act` is unable to locate Docker, make sure that the required `/var/run/docker.sock` symlink exists. If it does not, you can fix it by running:

    ```shell
    sudo ln -s "$HOME/.docker/run/docker.sock" /var/run/docker.sock`
    ```

12. *(Optional)* Build the documentation and PyPI package independent of deployment:

    ```shell
    make build
    ```
    
    ***Note***: You can run `make docs` to recreate documentation without building the PyPI package with `setup.py`.

13. *(Optional)* Check MkDocs documentation by serving it at [http://localhost:8000/](http://localhost:8000/) locally:

    ```shell
    make test_docs
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
    
17. *(Optional)* Test packages for PyPI deployment:

    ```shell
    make verify_build
    ```
    
18. *(Optional)* Test deployment by building the PyPI packages, recreating the documentation, and deploying to Test PyPI:

    ```shell
    make test_deploy
    ```

19. Deploy YFPY by building the PyPI packages, recreating the documentation, and deploying to PyPI:

    ```shell
    make deploy
    ```

20. Build Docker container:
    ```shell
    docker compose -f compose.yaml -f compose.build.yaml build
    ```

21. *(If needed)* Authenticate with GitHub Personal Access Token (PAT):
    ```shell
    jq -r .github_personal_access_token.value private-github.json | docker login ghcr.io -u uberfastman --password-stdin
    ```

22. Deploy the newly-built Docker image with respective major, minor, and patch version numbers to the GitHub Container Registry:
    ```shell
    docker push ghcr.io/uberfastman/yfpy:X.X.X
    ```

23. Create a second git commit with updated version number and documentation:

    ```shell
    git add .
    git commit -m 'update version number and docs'
    ```

24. Update YFPY GitHub repository:

    ```shell
    git push
    ```
