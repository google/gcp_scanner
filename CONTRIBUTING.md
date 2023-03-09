# How to Contribute

We'd love to accept your patches and contributions to this project. There are
just a few small guidelines you need to follow.

## Contributor License Agreement

Contributions to this project must be accompanied by a Contributor License
Agreement. You (or your employer) retain the copyright to your contribution;
this simply gives us permission to use and redistribute your contributions as
part of the project. Head over to <https://cla.developers.google.com/> to see
your current agreements on file or to sign a new one.

You generally only need to submit a CLA once, so if you've already submitted one
(even if it was for a different project), you probably don't need to do it
again.

## Code Reviews

All submissions, including submissions by project members, require review. We
use GitHub pull requests for this purpose. Consult
[GitHub Help](https://help.github.com/articles/about-pull-requests/) for more
information on using pull requests.

## Community Guidelines

This project follows [Google's Open Source Community
Guidelines](https://opensource.google/conduct/).

## Commit Message Conventions
- Start with a short summary (50 characters or less) of the changes made.
- Use the present tense and imperative mood.
- Separate the summary from the body of the message with a blank line.
- Use the body to explain what and why changes were made, as well as any necessary details.
- Addionally, you can consider using [semantic commit messages](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716?permalink_comment_id=3867882) like "feat:", "docs:", etc. which will provide additional context to the commit message.

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
- Add `issue tracker id`

**Example:** `feat/<issue-id>/gcp-compute-engine-support`