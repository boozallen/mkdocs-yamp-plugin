# Copyright 2022 Booz Allen Hamilton
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
from mkdocs.config import config_options as c
from mkdocs.config.base import Config
from mkdocs.exceptions import PluginError
from mkdocs.utils import warning_filter
from git import Repo

log = logging.getLogger("mkdocs.plugins." + __name__)
log.addFilter(warning_filter)

class RepoItem(Config):
  ### Configuration provided by mkdocs.yaml
  # the repository URL to clone
  url = c.Optional(c.Type(str, default = None))
  # the branch of the repository to clone
  branch = c.Type(str, default = "main")
  # a list of globs specifying paths within
  # the repository to clone
  include = c.ListOfItems(c.Type(str), default = [])

  # a relative path from the mkdocs.yaml file 
  # to a directory to include in the generated
  # 'temp_dir' directory via symlink
  path = c.Optional(c.Type(str))

  ### Configuration determined by self
  repo_name = None

  # validate the user-provided configuration
  def do_validation(self):
    # you must define either a URL or a path, but not both
    if not (self.url or self.path):
      raise PluginError(f'repo does not define a url or a path')
    
    if self.url and self.path:
      raise PluginError(f'repo cannot define both a url and a path')

  def fetch(self, temp_dir, first_build):
    if self.url:
      self.clone_git_repo(temp_dir, first_build)
    else:
      self.create_symlink(temp_dir)

  def clone_git_repo(self, temp_dir, first_build):
    self.repo_name = self.url.split("/")[-1].replace('.git','')
    # path to clone the repository to
    r_path = os.path.join(temp_dir, self.repo_name)
    if os.path.exists(r_path):
      # # do a git pull 
      self.log.info(f'git pull {self.url}')
      # r = Repo(r_path)
      # r.remotes.origin.pull()
    else: 
      # do a git clone
      if self.include:
        # equivalent to:
        #  git clone --no-checkout $repo
        #  cd $repo
        #  git checkout origin/main -- some_file.md some_directory/
        r = Repo.clone_from(self.url, r_path, no_checkout = True)
        if not self.branchExists(r, self.branch):
          raise PluginError(f'repository {self.url} does not have branch {self.branch}')
        else:
          git = r.git()
          git.checkout(f'origin/{self.branch}', "--", *self.include)
      else:
        r = Repo.clone_from(self.url, r_path)
        if not self.branchExists(r, self.branch):
          raise PluginError(f'repository {self.url} does not have branch {self.branch}')
        r.git.checkout(f'origin/{self.branch}')

  def branchExists(self, repo, branch):
    return f'origin/{branch}' in [ ref.name for ref in repo.references ]

  def set_edit_url(self, page, temp_dir):
    if self.url: 
      prefix = f'{temp_dir}/{self.repo_name}/'
      edit_url = ''.join([
        self.url.replace(".git", ""),
        "/edit/",
        f'{self.branch}/',
        page.file.src_path[len(prefix):]
      ])
      page.edit_url = edit_url
    else:
      page.edit_url = None

  def create_symlink(self, temp_dir):
    src = os.path.abspath(self.path)
    if not os.path.exists(src):
      raise PluginError(f'path {src} does not exist')
  
    self.repo_name = os.path.basename(src)
    dst = os.path.abspath(os.path.join(temp_dir, self.repo_name))
    if not os.path.exists(dst):
      os.symlink(src, dst, True)