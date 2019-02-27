workflow "Release to PyPi" {
  on = "release"
  resolves = ["upload"]
}

action "tag-filter" {
  uses = "actions/bin/filter@24a566c2524e05ebedadef0a285f72dc9b631411"
  args = "tag"
}

action "check" {
  uses = "ross/python-actions/setup-py/<python-version>@<commit-ish>"
  args = "check"
  needs = "tag-filter"
}

action "sdist" {
  uses = "ross/python-actions/setup-py/<python-version>@<commit-ish>"
  args = "sdist"
  needs = "check"
}

action "upload" {
  uses = "ross/python-actions/twine@<commit-ish>"
  args = "upload ./dist/<your-module-name>-*.tar.gz"
  secrets = ["TWINE_PASSWORD", "TWINE_USERNAME"]
  needs = "sdist"
}
