# How to Contribute

We'd love to accept your patches and contributions to this project. There are just a few small guidelines you need to follow.

## Contributor License Agreement

Contributions to this project must be accompanied by a Contributor License Agreement. You (or your employer) retain the copyright to your contribution; this simply gives us permission to use and redistribute your contributions as part of the project. Head over to [CLA](https://cla.developers.google.com/) to see your current agreements on file or to sign a new one.

You generally only need to submit a CLA once, so if you've already submitted one (even if it was for a different project), you probably don't need to do it again.

## Installation

Please refer [`INSTALL.md`](https://github.com/google/gcp_scanner/blob/main/INSTALL.md) for detailed installation guideline on the tool.

## Code Reviews

All submissions, including submissions by project members, require review. We use GitHub pull requests for this purpose. Consult [GitHub Help](https://help.github.com/articles/about-pull-requests/) for more information on using pull requests.

## Community Guidelines

This project follows [Google's Open Source Community Guidelines](https://opensource.google/conduct/).

## Commit Message Conventions

- Start with a short summary (50 characters or less) of the changes made.
- Use the present tense and imperative mood.
- Separate the summary from the body of the message with a blank line.
- Use the body to explain what and why changes were made, as well as any necessary details.
- Additionally, you can consider using [semantic commit messages](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716?permalink_comment_id=3867882) like "feat:", "docs:", etc. which will provide additional context to the commit message.

| Commit Type | Description |
| ---- | ---- |
| `feat` | New feature or functionality added |
| `fix` | Bug fix |
| `docs` | Changes to documentation |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks such as refactoring, dependencies updates, or removing unused code |
| `ci` | Changes to the build or continuous integration process |

**Example:** Add support for GCP Compute Engine in scanner

**Example:** feat: add support for GCP Compute Engine in scanner

**Example:** docs: updated README.md with installation instructions

**Example:** feat: added support for scanning additional GCP resources

**Example:** fix: fixed bug in scan logic for GCE instances

**Example:** test: added unit tests for new scan feature

**Example:** ci: updated build pipeline to include new dependency

**Example:** chore: removed unused code and refactored some variables

## Branching Naming Conventions

- Use lowercase letters.
- Separate words with hyphens.
- Use descriptive names that reflect the purpose of the branch.
- Add `issue tracker id`.

**Example:** feat/&lt;issue-id&gt;/gcp-compute-engine-support

**Example:** docs/11/update-installation-instructions
 
### Some other things to keep in mind before any PR

1. Check for linting using PyLint:
    - for first time do (to install a local copy of `pylintrc`):

    ```bash
    wget https://google.github.io/styleguide/pylintrc
    ```

    - to run `pylint` for `gcp_scanner`

    ```bash
    pylint --rcfile pylintrc --disable=W0703,R1734,R1735,C0209,C0103,R1732 src/gcp_scanner/*.py
    ```

2. Ensure that the corresponding tests are successful.

3. If any new features have been added, then check with GCP to ensure they work as expected.

## Getting Help

If you need help or have any questions about the project, please feel free to:

- Read the [project's documentation](https://github.com/google/gcp_scanner/blob/main/README.md).
- Open a new issue on the [project's GitHub repository](https://github.com/google/gcp_scanner/issues).
- Contact the project maintainers by posting to the [Google Group](https://groups.google.com/g/gcp-scanner).

## Code of Conduct

We believe in creating a friendly and welcoming environment for all members of our community. As such, we follow the [Google Open Source Community Guidelines](https://opensource.google/conduct/), which outlines our expectations for all those who participate in our project.

Please read the code of conduct carefully and make sure you understand what is expected of you. If you have any questions or concerns, please contact the project maintainers by posting to the [Google Group](https://groups.google.com/g/gcp-scanner).
