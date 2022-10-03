# Yet Another Multirepo Plugin

<div>
<a href="https://pypi.org/project/mkdocs-yamp/">
  <img src="https://img.shields.io/pypi/v/mkdocs-yamp?color=blue&style=flat-square">
</a>
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/mkdocs-yamp?style=flat-square">
</div>

This plugin allows users to define external repositories for integration into the MkDocs site.

Declared repositories are added to a subdirectory within your docs directory.

Users can then reference files within those repositories from their own navigation.

## Config

```yaml
plugins:
  - yamp:
    # directory within docs dir to add content
    temp_dir: "repos"
    # delete docs/{temp_dir} after build||serve?
    #  default: true
    cleanup: true
    # delete docs/{temp_dir} at the beginning of the
    # mkdocs invocation.
    start_fresh: true
    # declare a list of repositories or directories to add
    # to docs/{temp_dir}
    #   default: []
    repos:
      # the git repository URL to clone
    - url: "https://github.com/some-user/some-repo"
      # a list of globs to checkout
      # if empty or not provided, the entire repository is cloned
      # default: [ ]
      include: [ "README.md", "docs/index.md"]
      # the branch of the repository to clone
      branch: "main"

      # alternatively, you can provide a path.
      # a symlink will be created within docs/{temp_dir}
    - path: "../some-other-directory"
```

## Example Usage

```yaml
plugins:
  - search: {}
  - yamp:
      repos:
        - url: https://github.com/steven-terrana/mkdocs-b
          branch: develop
        - url: https://github.com/steven-terrana/mkdocs-a

# Page Tree
nav:
  - Home: 
    - index.md
    - repos/local-dir/README.md
  - Concepts:
    - concepts/index.md
    - repos/mkdocs-b/README.md
    - repos/mkdocs-a/docs/concepts/concept.md
```
