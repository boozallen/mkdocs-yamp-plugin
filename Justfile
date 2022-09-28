# the output directory for the documentation
docsDir  := "site"

# describes available recipes
help: 
  just --list --unsorted

# wipe local caches
clean: 
  rm -rf {{docsDir}} docs/repos

############################
# Release
############################
release version: 
  #!/usr/bin/env bash
  # validate currently on main
  branch="$(git branch --show-current)"
  if [[ ! "${branch}" == "main" ]]; then 
    echo "You can only cut a release from the 'main' branch."
    echo "Currently on branch '${branch}'"
    exit 1
  fi

  # validate currently in main repository
  origin=$(git remote get-url origin)
  if [[ ! "${origin}" == "https://github.com/boozallen/mkdocs-yamp-plugin" ]]; then
    echo "You must publish from the source repository"
    echo "Currently origin = ${origin}"
    exit 1
  fi

  # update the release version on the main branch
  hatch version {{version}}
  git add yamp/__init__.py
  version=$(hatch version)
  git commit -m "bumping version to ${version}"
  git push 

  # cut a release branch and cut a release tag
  git checkout -B release/{{version}}
  git push --set-upstream origin release/{{version}}
  git tag {{version}}
  git push origin refs/tags/{{version}}

  # publish the release to pypi
  source .pypi.env
  hatch build 
  hatch publish -r main

  # bump to rc candidate
  git checkout main
  hatch version patch,rc
  version=$(hatch version)
  git add yamp/__init__.py
  git commit -m "bump release to ${version}"
  git push

############################
# Documentation Recipes
############################

# builds the jte docs builder image
docsImage := "docs-builder"
buildDocsImage:
  docker build . -t {{docsImage}} 

# Build the jte documentation
docs: buildDocsImage
  docker run --rm -v $(pwd)/..:/docs -w /docs/$(basename $(pwd)) {{docsImage}} build

# serve the docs locally for development
serve: buildDocsImage
  docker run --rm -p 8000:8000 -v $(pwd)/..:/docs -w /docs/$(basename $(pwd)) {{docsImage}} serve -a 0.0.0.0:8000
