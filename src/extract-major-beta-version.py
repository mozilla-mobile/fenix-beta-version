#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/


import os, re, sys

from github import Github, InputGitAuthor, enable_console_debug_logging


#
# All these are lifted from relbot/utils.py
#


def major_version_from_fenix_release_branch_name(branch_name):
    if matches := re.match(r"^releases[_/]v(\d+)\.0\.0$", branch_name):
        return int(matches[1])
    raise Exception(f"Unexpected release branch name: {branch_name}")


def get_fenix_release_branches(repo):
    return [branch.name for branch in repo.get_branches()
            if re.match(r"^releases[_/]v\d+\.0\.0$", branch.name)]


def get_latest_fenix_version(repo):
    major_fenix_versions = [major_version_from_fenix_release_branch_name(branch_name)
                            for branch_name in get_fenix_release_branches(repo)]
    if len(major_fenix_versions) > 0:
        return sorted(major_fenix_versions, reverse=True)[0]


def is_beta_version(version):
    return re.compile(r'\d+.0.0-beta.\d+', re.MULTILINE).match(version)


def is_fenix_beta_branch(fenix_repo, release_branch_name):
    """Fetch version.txt from the given Fenix branch and throw an exception if it is not a Beta release"""
    content_file = fenix_repo.get_contents("version.txt", ref=release_branch_name)
    version = content_file.decoded_content.decode('utf8')
    return is_beta_version(version)


#
# Main Action starts here. It expects GITHUB_TOKEN and
# GITHUB_REPOSITORY_OWNER to be set.
#

if __name__ == "__main__":

    github = Github()
    if github.get_user() is None:
        print("[E] Could not get authenticated user. Exiting.")
        sys.exit(1)

    verbose = os.getenv("VERBOSE") == "true"

    organization = os.getenv("GITHUB_REPOSITORY_OWNER")
    if not organization:
        print("[E] No GITHUB_REPOSITORY_OWNER set. Exiting.")
        sys.exit(1)

    fenix_repo = github.get_repo(f"{organization}/fenix")

    if verbose:
        print(f"[I] Looking at Fenix at {fenix_repo.full_name}")

    #
    # Actual Action logic starts here. The strategy is very simple:
    #
    # - Find the latest Fenix release (branch with highest major release number)
    # - Look at version.txt to make sure that branch is actually in Beta
    #

    latest_fenix_version = get_latest_fenix_version(fenix_repo)
    if not latest_fenix_version:
        print(f"[E] Could not determine current A-C version on {organization}/fenix")
        sys.exit(1)

    branch_name = f"releases_v{latest_fenix_version}.0.0"

    if verbose:
        print(f"[I] Looking at Fenix branch {organization}/fenix:{branch_name}")

    if not is_fenix_beta_branch(fenix_repo, branch_name):
        print(f"Branch {organization}/fenix:{branch_name} is not in beta; returning an empty version")
        latest_fenix_version = ""

    print(f"::set-output name=fenix-beta-version::{latest_fenix_version}")

