# Changelog

## [1.0.1](https://github.com/google/gcp_scanner/compare/v1.0.0...v1.0.1) (2023-03-29)


### Miscellaneous

* Enable release to PyPI ([45c22a1](https://github.com/google/gcp_scanner/commit/45c22a134f968f407e9e7c618ddc0359cec40ba5))
* fix PyPI release ([4cf77a5](https://github.com/google/gcp_scanner/commit/4cf77a55c048a2b055e95d29783cfaf09f2d9862))
* Remove extra build from PyPI release ([278e41a](https://github.com/google/gcp_scanner/commit/278e41a0f87a23fb27a6706ec8a2cfbdce5220a4))
* Removing extra PyPI release file. ([79c3f47](https://github.com/google/gcp_scanner/commit/79c3f47117ea33ff6cea972f94b098d32def7a37))

## 1.0.0 (2023-03-29)


### Features

* added list cloud source repo functionalities in the scanner ([#19](https://github.com/google/gcp_scanner/issues/19)) ([4eb3ba6](https://github.com/google/gcp_scanner/commit/4eb3ba6bbee9edc3f4482502fd23539b44e60f1a))
* added list cloud source repo functionalities in the scanner ([#19](https://github.com/google/gcp_scanner/issues/19)) ([df8e1ee](https://github.com/google/gcp_scanner/commit/df8e1ee2e8aa2b4ec0ede2928ab581362f17228a))
* crawler for cloud dns policies ([#56](https://github.com/google/gcp_scanner/issues/56)) ([413aa5f](https://github.com/google/gcp_scanner/commit/413aa5f0fb8547d3ecadadf7a871456110f9383c))
* dummped token_scope in the result for informational perpose ([#21](https://github.com/google/gcp_scanner/issues/21)) ([eef5a93](https://github.com/google/gcp_scanner/commit/eef5a93cbe845cc951e246db0ddb5b6615a74ab1))
* error handling implemented ([#21](https://github.com/google/gcp_scanner/issues/21)) ([0529f0a](https://github.com/google/gcp_scanner/commit/0529f0a6e94da1526210874f816ec567b826ee6e))
* fix lint ([#21](https://github.com/google/gcp_scanner/issues/21)) ([fe8f4dc](https://github.com/google/gcp_scanner/commit/fe8f4dc8d6bd679c31ddbe7bbae64ef49ffa5ab5))
* implemented crawler for listing cloud source repositories ([#19](https://github.com/google/gcp_scanner/issues/19)) ([3ca9933](https://github.com/google/gcp_scanner/commit/3ca9933872d9e83cc30932297e416b5b8dd010a1))
* log to a specified path ([90bbace](https://github.com/google/gcp_scanner/commit/90bbacea189445b0a5a1775e54c1fcb803a04c9c))
* moved PR template under .github directory. ([2c9f7e1](https://github.com/google/gcp_scanner/commit/2c9f7e137385f8ea05467e5d4f9ba88235da7d6d))
* obtaining scope from a refresh token ([#21](https://github.com/google/gcp_scanner/issues/21)) ([31c2ecc](https://github.com/google/gcp_scanner/commit/31c2ecc19bf9da4d2bc4871cf43662b1a2110a6f))
* prepared pyproject for deploying in pypi ([#89](https://github.com/google/gcp_scanner/issues/89)) ([f5cfa84](https://github.com/google/gcp_scanner/commit/f5cfa84664b595fd8a9ea771315de29b0ebf0a08))
* removed enforing scope when no scope is provided ([#21](https://github.com/google/gcp_scanner/issues/21)) ([8c42bbf](https://github.com/google/gcp_scanner/commit/8c42bbf677b4f27aebd65f93ee41cda2b25308d9))
* unit test implemented for get_scopes_from_refresh_token ([#21](https://github.com/google/gcp_scanner/issues/21)) ([c5541b8](https://github.com/google/gcp_scanner/commit/c5541b8bf672ce7af19d622dec09f2e52181b4bd))
* updated example config ([#19](https://github.com/google/gcp_scanner/issues/19)) ([e7d1e94](https://github.com/google/gcp_scanner/commit/e7d1e94dd46d5bf6cce069682e502d2877d97fdd))
* updated maxPage size for each req to 500 ([#19](https://github.com/google/gcp_scanner/issues/19)) ([5596100](https://github.com/google/gcp_scanner/commit/5596100cd4f0aa1719b13b285af894fa9fe9acbb))
* updated method name wording ([#21](https://github.com/google/gcp_scanner/issues/21)) ([3217c7d](https://github.com/google/gcp_scanner/commit/3217c7d958e7e61347580710799efe05db7d5136))


### Bug Fixes

* [#114](https://github.com/google/gcp_scanner/issues/114) ([20b1051](https://github.com/google/gcp_scanner/commit/20b1051808517953677a0a45e20280983d5de47a))
* docstring updated to mach with the function args. ([87766bf](https://github.com/google/gcp_scanner/commit/87766bf3e000b14946d79b498cf913d095420dbd))
* enclosed in a list ([a9b552d](https://github.com/google/gcp_scanner/commit/a9b552dddc0ad2c139ac7fc9350944de2113b55f))
* fixed  bug on paginated response from cloudsource list api.([#19](https://github.com/google/gcp_scanner/issues/19)) ([6539f90](https://github.com/google/gcp_scanner/commit/6539f9055f7fae08540968462e2dbe4fc88c392f))
* fixed spelling mistakes in the list_services log message. ([f990475](https://github.com/google/gcp_scanner/commit/f990475c3aa0c9e23a074ddd6f73fe95df46c13a))
* indentation in CONTRIBUTING.md ([63c5cac](https://github.com/google/gcp_scanner/commit/63c5cac2c6a17ba19b462651650c3a3da3bfdc1a))
* linting error fixed ([#19](https://github.com/google/gcp_scanner/issues/19)) ([2ae064f](https://github.com/google/gcp_scanner/commit/2ae064fc17808ce128f39c59fb641b2dc1bf91d3))
* logging fixed ([6c410ae](https://github.com/google/gcp_scanner/commit/6c410aec951d3c73e48b5fd5a1b972eb63ef4b12))
* machineImages() ([243068d](https://github.com/google/gcp_scanner/commit/243068d35701df0943171b4fad7054c2fa7cee0a))
* type in the docstring of crawl and scanner module fixed. ([f5f46b2](https://github.com/google/gcp_scanner/commit/f5f46b220d4a3bb959288c122a38abfec5c430a5))
* update packages to the latest version available ([405a6d0](https://github.com/google/gcp_scanner/commit/405a6d03a542d278946deb7016ebeeec51014aaf))
* updated docstring for GKE cluster crawler. ([a979f03](https://github.com/google/gcp_scanner/commit/a979f03211ca2e219e8c3cd8990c025d2f937af5))
* use lazy % formatting ([d405a0c](https://github.com/google/gcp_scanner/commit/d405a0c24793e47a1674dde52c6e9a553688ccb5))
* use python3.10.10 Dockerfile ([026eda0](https://github.com/google/gcp_scanner/commit/026eda03575ae6ecdf28afd81f8e04ab948b5ce1))


### Miscellaneous

* add .vscode directory to .gitignore file ([a001140](https://github.com/google/gcp_scanner/commit/a001140812e648003b74b59e4e96d0309102b923))
* added endlne in the file ([#89](https://github.com/google/gcp_scanner/issues/89)) ([73ea401](https://github.com/google/gcp_scanner/commit/73ea401c9283d55c97ff66d7c41c7cc0ca223483))
* issue template for github added ([e141f8c](https://github.com/google/gcp_scanner/commit/e141f8c76733e31331b4747100608dd302dd3757))
* moved pr template to the root of .github directory as PR_TEMPLATE foldering not supported under the .github directory ([a5e3e34](https://github.com/google/gcp_scanner/commit/a5e3e34b0e60c48c34efa93067222a0b7530db80))
* name updated with hyphen ([#89](https://github.com/google/gcp_scanner/issues/89)) ([c1f96f5](https://github.com/google/gcp_scanner/commit/c1f96f53c9bf315a71fcbf855a85d20722295f95))
* project description updated ([#89](https://github.com/google/gcp_scanner/issues/89)) ([c211feb](https://github.com/google/gcp_scanner/commit/c211febc9c5188a1791eeb5c44522674dfffa36d))
* workflow for publishing into pypi added ([#89](https://github.com/google/gcp_scanner/issues/89)) ([27f382b](https://github.com/google/gcp_scanner/commit/27f382bd3c63001c78dad7b2a09caa6ef21b0d68))


### Documentation

* add commit and branching naming conventions to contributing.md ([de3ced8](https://github.com/google/gcp_scanner/commit/de3ced865ca3c7534e3d2df9e0eb3e57afe92533))
* add pull request template ([103cbd0](https://github.com/google/gcp_scanner/commit/103cbd0cbad74ceff8aa04b891351cbf41f71886))
* Fix spaces after comma ([e085ee2](https://github.com/google/gcp_scanner/commit/e085ee29ccd3698124ad56ed740d23d551fa99b0))
* fixed CONTRIBUTING.md formatting error ([e02d939](https://github.com/google/gcp_scanner/commit/e02d9395a6d6199b9a9c3817c6cf5d4509bd428a))
* fixed minor spelling and grammartical issues in the readme.md ([#26](https://github.com/google/gcp_scanner/issues/26)) ([2b80564](https://github.com/google/gcp_scanner/commit/2b8056471e9f0984d2d837496244e4442c13e82a))
* update &lt;issue-id&gt; for branch naming conventions ([c7c74af](https://github.com/google/gcp_scanner/commit/c7c74af5f5489425e5314adea52b4034cb81a152))
* update contributing.md ([f71d1b8](https://github.com/google/gcp_scanner/commit/f71d1b883b9ff8d6d92f0af1039c414d52a7e38d))
* update CONTRIBUTING.md ([dbddc44](https://github.com/google/gcp_scanner/commit/dbddc44643addd0c103b0d9bb2806862f3b1cac6))
* Update CONTRIBUTING.md file ([1fcb8da](https://github.com/google/gcp_scanner/commit/1fcb8da154e1749cd463ec0ec32e586c676879d8))
* Update CONTRIBUTING.md file ([13d6fe6](https://github.com/google/gcp_scanner/commit/13d6fe695304062a9fa902953ddcdfe6d8da5ee0))
* update contributing.md with examples for semantic messages ([2b14b2a](https://github.com/google/gcp_scanner/commit/2b14b2a813de368e115499c2401180a7b68fc894))
* updated bug report example to align with gcp scanner ([8368552](https://github.com/google/gcp_scanner/commit/8368552006cbb448fe4ee20b9a100596d8684c46))
* updated README.md with python-client version ([da6113d](https://github.com/google/gcp_scanner/commit/da6113de2a1e5878e76deafec31bd0c7fb1761b2))


### Tests

* added integration test boilerplate for get_refresh_token_scope ([4fffc79](https://github.com/google/gcp_scanner/commit/4fffc799c9634630d176e17b22decea7ae845843))
* example sourcerepos file added for testing; update according to the test poject  ([#19](https://github.com/google/gcp_scanner/issues/19)) ([38dfa1a](https://github.com/google/gcp_scanner/commit/38dfa1a7a02fe6c7b35bcd3946f6e21850628db1))
* Fix failing services test ([f2dcbdf](https://github.com/google/gcp_scanner/commit/f2dcbdf1d0b9ff2a54772482dba6528b6ad90057))
* linting errors fixed ([#14](https://github.com/google/gcp_scanner/issues/14)) ([3292c4c](https://github.com/google/gcp_scanner/commit/3292c4cdfd9d6afa109409f98dbaddd1c2fc1bf6))
* refactored crawler unittests ([#14](https://github.com/google/gcp_scanner/issues/14)) ([cb9aa0d](https://github.com/google/gcp_scanner/commit/cb9aa0d733ede5bda4a5b6017e33c7a0e5500e13))
* unit test added for cloud source repo crawler ([#19](https://github.com/google/gcp_scanner/issues/19)) ([995b591](https://github.com/google/gcp_scanner/commit/995b59160a808428fff1c91c5dc2104b120ad184))
* updated docstring typo ([55884ab](https://github.com/google/gcp_scanner/commit/55884ab3ef335cd50aeb647ab1f8fbf16301dc5e))
* updated test boilerplate for integration tes of the get RT ([#69](https://github.com/google/gcp_scanner/issues/69)) ([f5f12b4](https://github.com/google/gcp_scanner/commit/f5f12b434cc2548f650cdd591f73beef44551c26))
* updated test/sourcerepos file ([#19](https://github.com/google/gcp_scanner/issues/19)) ([6c80db3](https://github.com/google/gcp_scanner/commit/6c80db3cfc9a59db5176a9884c6efe79a576b75c))
* updated unit test ([#19](https://github.com/google/gcp_scanner/issues/19)) ([01ec811](https://github.com/google/gcp_scanner/commit/01ec811e21ccae49db4d1f6625bfe3d957938c70))
