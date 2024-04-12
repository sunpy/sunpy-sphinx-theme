"""
Run all builds for all active versions of all SunPy and SunPy subprojects on
RTD.
"""

import os

import requests

ORG_PROJECT = "sunpy"
BASE_URL = "https://readthedocs.org/api/v3/projects/"
HEADERS = {"Authorization": f"Token {os.environ['RTD_AUTH_TOKEN']}"}
# RTD removes the full stop from the project slug
WEBSITE_PROJECT = "sunpyorg"


def get_active_versions(project):
    r = requests.get(f"{BASE_URL}{project}/versions", headers=HEADERS, params={"active": True})
    if not r.ok:
        print(f"Failed to get versions for {project}: {r}")
        return []
    r = r.json()
    if "results" not in r:
        print(project)
        print(r)
        return []
    results = r["results"]
    return [res["slug"] for res in results]


def get_all_subprojects(base_project):
    r = requests.get(f"{BASE_URL}{base_project}/subprojects", headers=HEADERS)
    r = r.json()
    results = r["results"]
    return [res["child"]["slug"] for res in results]


def rebuild_all_versions_for_project(project):
    slugs = get_active_versions(project)
    for slug in slugs:
        r = requests.post(f"{BASE_URL}{project}/versions/{slug}/builds/", headers=HEADERS)
        if r.status_code != 202:
            print(f"{slug} failed to build with: {r}")


if __name__ == "__main__":
    projects = [ORG_PROJECT, *get_all_subprojects(ORG_PROJECT), WEBSITE_PROJECT]
    for project in projects:
        rebuild_all_versions_for_project(project)
