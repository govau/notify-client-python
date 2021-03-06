<!--Thanks for contributing to Notify.gov.au. Using this template to write your pull request message will help get it merged as soon as possible. -->

## What problem does the pull request solve?

<!--- Describe why you’re making this change -->

## Checklist

<!--- All of the following are normally needed. Don’t worry if you haven’t done them or don’t know how – someone from the Notify team will be able to help. -->

- [x] I’ve used the pull request template
- [ ] I’ve written unit tests for these changes
- [ ] I’ve update the documentation in
  - [ ] `DOCUMENTATION.md`
  - [ ] `CHANGELOG.md`
  - [ ] `Notify docs: https://github.com/govau/notify/blob/master/docs/src/code-examples/setup-install/python.mdx`
- [ ] I’ve bumped the version number in
  - [ ] `notify/__init__.py`
  - [ ] `tests/notify_python_client/test_base_api_client.py`, function `test_user_agent_is_set`
- [ ] I've added new environment variables to
  - [ ] `scripts/generate_docker_env.sh`
  - [ ] `tox.ini`
  - [ ] `CONTRIBUTING.md`
