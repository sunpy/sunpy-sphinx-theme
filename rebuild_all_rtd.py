"""
Run all builds for all active versions of all SunPy and SunPy subprojects on
RTD.
"""

import os

import requests

BASE_PROJECT = "sunpy"
BASE_URL = "https://readthedocs.org/api/v3/projects/"
TOKEN = os.environ["RTD_AUTH_TOKEN"]
headers = {"Authorization": f"Token {TOKEN}"}


def get_active_versions(project):
    r = requests.get(
        f"{BASE_URL}{project}/versions",
        headers=headers,
        params={"active": True},
    )
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
    r = requests.get(f"{BASE_URL}{base_project}/subprojects", headers=headers)
    r = r.json()
    results = r["results"]
    return [res["child"]["slug"] for res in results]


def rebuild_all_versions_for_project(project):
    slugs = get_active_versions(project)
    for slug in slugs:
        r = requests.post(f"{BASE_URL}{project}/versions/{slug}/builds/", headers=headers)
        if r.status_code != 202:
            print(f"{slug} failed to build with: {r}")


if __name__ == "__main__":
    projects = [BASE_PROJECT] + get_all_subprojects(BASE_PROJECT)
    for project in projects:
        rebuild_all_versions_for_project(project)
