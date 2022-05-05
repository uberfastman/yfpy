# YFPY Deployment

1. Clear virtual machine of old requirements:

    ```shell
    pip uninstall -y -r <(pip freeze)    
    ```

2. Check `requirements.txt` for latest dependency versions.
3. Update virtual machine with latest dependencies:

    ```shell
    pip install -r requirements.txt    
    ```

4. (Optional) Update a `dev-requirements.txt` file:

    ```shell
    pip freeze > dev-requirements.txt
    ```

5. Lint code with `flake8`:

    ```shell
    flake8 . --count --show-source --statistics
    ```

6. Check code security with `bandit`:

    ```shell
    bandit -r yfpy/
    ```

7. Run *all* `pytest` tests (see following commands for running subsets of tests):

    ```shell
    python -m pytest
    ```

8. Run *all* `pytest` tests *verbosely*:

    ```shell
    python -m pytest -v -s
    ```

9. Run `pytest` unit tests:

    ```shell
    python -m pytest -v -s -m unit 
    ```

10. Run `pytest` integration tests:

     ```shell
     python -m pytest -v -s -m integration 
     ```

11. (Optional) Run all tests from `pytest` file:

     ```shell
     python -m pytest -v -s -m integration test/integration/test_api_game_data.py
     ```

12. (Optional) Run *specific* test from `pytest` file:

     ```shell
     python -m pytest -v -s -m integration test/integration/test_api_game_data.py -k test_get_game_key_by_season
     ```

13. Update the Sphinx documentation:

     ```shell
     cd docs-sphinx
     ```

     ```shell
     make html    
     ```
   
14. Check Sphinx documentation locally:

     ```shell
     open build/html/index.html    
     ```
   
15. Navigate to root directory:

     ```shell
     cd ..    
     ```

16. Execute `git add .`, `git commit -m 'commit message'`, and `git push`.

17. Update the git tag:

     `git tag -a [tag_name/version] -m [message]`

     ```shell
     git tag -a v1.0.0 -m 'first release'    
     ```
   
     ```shell
     git push origin --tags    
     ```

18. Build the package (will also auto-update the version based on teh above git tag):

     ```shell
     python setup.py sdist bdist_wheel
     ```

19. Once more execute `git add .`, `git commit -m 'commit message'`, and `git push`.

20. Install `twine` (if not already installed):

     ```shell
     pip install twine
     ```

21. Check packages before distribution:

    ```shell
    twine check dist/*
    ```

22. Deploy to Test PyPI to check:

     ```shell
     twine upload -r testpypi dist/*
     ```

23. Deploy to PyPI:

     ```shell
     twine upload dist/*
     ```
