# Build steps
Building the project is done using `uv`. The following steps are followed to build and release a new version on github.

## Increment the `version` in `pyproject.toml`
Increment `version` in `pyproject.toml` in accordance with observed convention and common sense. Then save the file.  
  
## Build the project
Run from the project root:
```sh
uv build
```  
  
This will create build artifacts in `./dist` and make the project installable.  
  
## Remove `./dist/.gitignore`
uv creates this extra .gitignore to prevent pushing artifacts to git. To make a release installable from github this extra gitignore needs to be removed.  
  
```sh
rm ./dist/.gitignore
```  
  
## Commit, Tag, then push
1. Commit with a release message like: `Release: 0.1.0a1`
```sh
git commit -m `Release: 0.1.0a1`
```  
2. Tag the commit with the version
```sh
git tag -a 0.1.0a1 -m 'Release with feature x'
```  
3. Push, including tags
```sh
git push origin --tags
```  
  
## Optionally: Install new version in other projects
If you're using this package in other projects, install the new version.
```sh
uv add my_package_title --upgrade-package my_package_title
```
