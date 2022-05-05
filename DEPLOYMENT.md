# YFPY Deployment

1. Update the git tag:

    `git tag -a [tag_name/version] -m [message]`

    ```shell
    git tag -a v1.0.0 -m 'first release'    
    ```
   
    ```shell
    git push origin --tags    
    ```
   
2. Push updates to git.

3. Build the package (will also auto-update the version based on teh above git tag):

    ```shell
    python setup.py sdist bdist_wheel
    ```

4. Check packages before distribution:

   ```shell
   twine check dist/*
   ```

5. Deploy to Test PyPI to check:

    ```shell
    twine upload -r testpypi dist/*
    ```

6. Deploy to PyPI:

    ```shell
    twine upload dist/*
    ```
