workflow "Release to PyPi" {
  on = "release"
  resolves = ["Run Twine Upload"]
}

action "Run Setup.py" {
  uses = "\"ross/python-actions/setup-py/<python-version>@<commit-ish>\""
}

action "Run Twine Upload" {
  uses = "\"ross/python-actions/twine@<commit-ish>\""
  needs = ["Run Setup.py"]
  secrets = ["GITHUB_TOKEN", "TWINE_USERNAME", "TWINE_PASSWORD"]
}
