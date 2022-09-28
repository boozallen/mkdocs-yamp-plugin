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
publish: 
  # hatch build
  # hatch publish -r test

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
