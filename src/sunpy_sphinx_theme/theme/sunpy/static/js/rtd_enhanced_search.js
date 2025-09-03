/*
    SunPy's enhanced search using ReadTheDocs
    Created: 2025-05
    Author: Stuart Lowe

    This script will augment the built-in search.

    You can provide an array of projects to a `set_search_config`.
    For example, you could add the following to the page:

    ```
    <script>
    const set_search_config = {
        "no-results":{
            "label":"Nothing to show here."
        },
        "load-more":{
            "label": "Load more results",
            "class": "btn btn-lg btn-sunpy btn-sunpy1"
        },
        "projects":[
            {"name":"sunpy","link":"https://docs.sunpy.org/"},
            {"name":"ndcube","link":"https://docs.sunpy.org/projects/ndcube/"},
            {"name":"sunraster","link":"https://docs.sunpy.org/projects/sunraster/"},
            {"name":"aiapy","link":"https://aiapy.readthedocs.io/"}
        ]
    };
    </script>
    ```
    where:
      * no-results - an optional object to set the label that gets displayed when there are no results
      * load-more - an optional object to set the class/label of the "load more" button
      * projects - an ordered array of projects to include (if empty this will be constructed from the ".nav-link" items found within #Documentation)

*/
/*jshint esversion: 6 */
(function (root) {
  function ready(fn) {
    if (document.readyState != "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  function Search(dialog, config) {
    // Set some defaults if not provided
    if (!config) config = {};
    if (!config.all) config.all = "All";
    if (!config["no-results"]) config["no-results"] = {};
    if (!config["no-results"].label)
      config["no-results"].label = "There are no results";
    if (!config["load-more"]) config["load-more"] = {};
    if (!config["load-more"].class)
      config["load-more"].class = "btn sd-btn sd-bg-primary sd-bg-text-primary";
    if (!config["load-more"].label)
      config["load-more"].label = "Load more results";

    let _obj = this;

    let debug = location.search.match(/debug/) ? true : false;

    this.results = {};
    this.tabs = {};
    this.selectedPanel = config.all;
    let icons = {
      filter:
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M1.5 1.5A.5.5 0 0 1 2 1h12a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.128.334L10 8.692V13.5a.5.5 0 0 1-.342.474l-3 1A.5.5 0 0 1 6 14.5V8.692L1.628 3.834A.5.5 0 0 1 1.5 3.5z"/></svg>',
      book: '<svg width="16" height="16" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M96 0C43 0 0 43 0 96V416c0 53 43 96 96 96H384h32c17.7 0 32-14.3 32-32s-14.3-32-32-32V384c17.7 0 32-14.3 32-32V32c0-17.7-14.3-32-32-32H384 96zm0 384H352v64H96c-17.7 0-32-14.3-32-32s14.3-32 32-32zm32-240c0-8.8 7.2-16 16-16H336c8.8 0 16 7.2 16 16s-7.2 16-16 16H144c-8.8 0-16-7.2-16-16zm16 48H336c8.8 0 16 7.2 16 16s-7.2 16-16 16H144c-8.8 0-16-7.2-16-16s7.2-16 16-16z"></path></svg>',
    };

    // Build the list of projects
    this.projects = {};
    this.projects[config.all] = { name: config.all, url: "" };
    if (config.projects) {
      this.projectorder = [config.all];
      // Use a provided array of objects containing "name" and "url"
      for (let p = 0; p < config.projects.length; p++) {
        let slug = config.projects[p].name;
        this.projectorder.push(slug);
        this.projects[slug] = { name: slug, url: config.projects[p].url };
      }
    } else {
      // Use the documentation nav links
      document
        .getElementById("Documentation")
        .querySelectorAll(".nav-link")
        .forEach(function (el) {
          // We might want to somehow limit which projects to include in the search
          let slug = el.innerHTML.replace(/(^\s|\s$)/, "");
          let link = el.getAttribute("href");
          _obj.projects[slug] = { name: slug, url: link };
        });
      this.projectorder = Object.keys(this.projects);
    }

    // Find the form/input
    const form = dialog.querySelector("form");
    const inp = form.querySelector("input[type=search]");

    const holder = document.createElement("div");
    holder.classList.add("readthedocs-search");
    form.replaceWith(holder);
    holder.appendChild(form);

    const content = document.createElement("div");
    content.classList.add("content", "bd-search-container");
    content.setAttribute("tabindex", -1);
    holder.appendChild(content);

    // Create a tablist container
    const tablist = document.createElement("div");
    tablist.classList.add("tablist");
    tablist.setAttribute("role", "tablist");
    tablist.setAttribute("tabindex", "-1");
    tablist.setAttribute("aria-label", "Project");
    content.appendChild(tablist);

    // Create a results container
    const results = document.createElement("div");
    results.classList.add("results");
    content.appendChild(results);

    // Create the search footer
    const footer = document.createElement("div");
    footer.classList.add("footer");
    footer.innerHTML = `<ul class="help" id="pyhc-search-help">
			<li><kbd>Enter</kbd> to select</li>
			<li><kbd>Up</kbd>/<kbd>Down</kbd> to navigate results</li>
			<li id="tab-help-item" style="display: none;"><kbd>Left</kbd>/<kbd>Right</kbd> to switch tabs</li>
			<li><kbd>Esc</kbd> to close</li>
			</ul>
			<div>
			<a href="https://docs.readthedocs.com/platform/stable/server-side-search/syntax.html#special-queries" target="_parent">View search syntax</a>
			</div>
			<div class="credits">
			Enhanced by
			<a href="https://about.readthedocs.com/">
				<svg version="1.1" viewBox="694 197 2e3 400" xmlns="http://www.w3.org/2000/svg"><g transform="matrix(.55754 0 0 .55754 68.308 1050.1)"><title>ReadTheDocs</title><path d="m1408.1-1181.7c-7.5 1-12.7 7.8-11.7 15.3 0.7 5.4 4.6 9.9 9.9 11.3 0 0 33.2 11 89.7 15.6 45.4 3.7 96.9-3.2 96.9-3.2 7.5-0.2 13.5-6.5 13.2-14s-6.5-13.5-14-13.2c-0.9 0-1.8 0.1-2.6 0.3 0 0-50.4 6.2-91.3 2.9-54-4.4-83.4-14.3-83.4-14.3-2.2-0.7-4.5-1-6.7-0.7zm0-67.6c-7.5 1-12.7 7.8-11.7 15.3 0.7 5.4 4.6 9.9 9.9 11.3 0 0 33.2 11 89.7 15.6 45.4 3.7 96.9-3.2 96.9-3.2 7.5-0.2 13.5-6.5 13.2-14s-6.5-13.5-14-13.2c-0.9 0-1.8 0.1-2.6 0.3 0 0-50.4 6.2-91.3 2.9-54-4.4-83.4-14.3-83.4-14.3-2.2-0.7-4.5-1-6.7-0.7zm0-67.6c-7.5 1-12.7 7.8-11.7 15.3 0.7 5.4 4.6 9.9 9.9 11.3 0 0 33.2 11 89.7 15.6 45.4 3.7 96.9-3.2 96.9-3.2 7.5-0.2 13.5-6.5 13.2-14s-6.5-13.5-14-13.2c-0.9 0-1.8 0.1-2.6 0.3 0 0-50.4 6.2-91.3 2.9-54-4.4-83.4-14.3-83.4-14.3-2.2-0.7-4.5-1-6.7-0.7zm0-67.5c-7.5 1-12.7 7.8-11.7 15.3 0.7 5.4 4.6 9.9 9.9 11.3 0 0 33.2 11 89.7 15.6 45.4 3.7 96.9-3.2 96.9-3.2 7.5-0.2 13.5-6.5 13.2-14s-6.5-13.5-14-13.2c-0.9 0-1.8 0.1-2.6 0.3 0 0-50.4 6.2-91.3 2.9-54-4.4-83.4-14.3-83.4-14.3-2.2-0.8-4.5-1-6.7-0.7zm-94.7-71.3c-71 0.5-97.5 22.3-97.5 22.3v530.3s25.8-22.3 109-18.9 100.3 32.6 202.5 34.6c102.2 2.1 127.9-15.7 127.9-15.7l1.5-540.6s-46 13-135.5 13.7-111-22.8-193.2-25.5c-5.1-0.1-10-0.2-14.7-0.2zm59.4 34.6s43 14.2 122.5 18.2c67.2 3.3 134.5-6.6 134.5-6.6v480.5s-34.1 17.9-119.3 11.8c-66-4.7-138.7-29.7-138.7-29.7l1-474.2zm-41.5 12.5c7.6 0 13.7 6.2 13.7 13.7s-6.2 13.7-13.7 13.7c0 0-22.3 0.1-35.8 1.5-22.8 2.3-38.3 10.6-38.3 10.6-6.7 3.5-15 1-18.5-5.7s-1-15 5.7-18.5c0 0 20.2-10.7 48.4-13.5 16.3-1.7 38.5-1.8 38.5-1.8zm-13.2 67.8c7.6-0.2 13.3 0 13.3 0 7.5 0.9 12.9 7.8 12 15.3-0.8 6.3-5.7 11.2-12 12 0 0-22.3 0.1-35.8 1.5-22.8 2.3-38.3 10.6-38.3 10.6-6.7 3.5-15 0.9-18.5-5.8s-0.9-15 5.8-18.5c0 0 20.2-10.7 48.4-13.5 7.9-0.9 17.5-1.4 25.1-1.6zm13.2 67.5c7.6 0 13.7 6.2 13.7 13.7 0 7.6-6.2 13.7-13.7 13.7 0 0-22.3-0.1-35.8 1.2-22.8 2.3-38.3 10.6-38.3 10.6-6.7 3.5-15 0.9-18.5-5.8s-0.9-15 5.8-18.5c0 0 20.2-10.7 48.4-13.5 16.2-1.5 38.4-1.4 38.4-1.4z" fill="currentColor"/></g><g fill="currentColor"><path d="m1128.6 491.9v-21.9l8.9-0.8c5.2-0.5 7.8-3.1 7.8-7.6v-125.6l-15.4-0.8v-23h73.8c20.9 0 36.9 3.9 48.1 11.6s16.8 20.5 16.8 38.1c0 12.3-3.2 22.3-9.7 30.3-6.3 7.9-13.9 13.7-22.7 17.3 6.5 2.3 11.6 7.8 15.4 16.5l19.5 42.4 15.4 0.5v23h-66.8v-21.9l7.8-0.8c4.1-0.5 6.2-2.2 6.2-4.9 0-1.1-0.4-2.3-1.1-3.8l-12.7-27c-2-4.5-4.2-7.7-6.8-9.5-2.3-2-5.8-3-10.3-3h-24.6v47l17.6 0.8v23l-67.2 0.1m49.7-96.5h23.5c22.2 0 33.2-9.9 33.2-29.7 0-11.4-3-18.7-8.9-22.2-5.8-3.4-15.1-5.1-28.1-5.1h-19.7v57"/><path d="m1356 351.9c13.5 0 24.2 3.3 32.2 10 7.9 6.5 11.9 15.7 11.9 27.6 0 7.9-1.7 15-5.1 21.1-3.4 5.9-7.7 10.6-12.7 14.1-5 3.4-11.2 6.2-18.4 8.4-12.1 3.6-25.7 5.4-40.8 5.4 0.5 9.5 3.5 17.3 8.9 23.2 5.4 5.8 13.7 8.6 24.9 8.6s22.3-4 33.5-11.9l10.3 21.9c-3.6 3.2-9.7 6.6-18.4 10-8.5 3.4-18.2 5.1-29.2 5.1-22 0-38.1-6-48.4-18.1-10.3-12.3-15.4-29-15.4-50.3s5.9-39.1 17.6-53.5c11.6-14.4 28-21.6 49.1-21.6m-12.4 61.9c6.7-1.3 12.8-3.9 18.4-7.8 5.6-4.1 8.4-9 8.4-14.6 0-11-5.4-16.5-16.2-16.5-10.1 0-17.8 4.1-23.2 12.2-5.4 7.9-8.4 17.5-8.9 28.6 7.8-0.2 15-0.8 21.5-1.9"/><path d="m1529.6 361.4v100.5c0 2.9 0.5 4.9 1.4 5.9 1.1 1.1 2.9 1.7 5.4 1.9l8.6 0.5v21.6h-43v-15.7l-0.8-0.3c-9 13-21.4 19.5-37 19.5-18.4 0-32-5.9-40.8-17.6s-13.2-27.7-13.2-48.1c0-24.5 5.9-43.6 17.8-57.3s29.7-20.5 53.5-20.5c15.3 0.1 31.4 3.3 48.1 9.6m-31.3 87.5v-70c-5-2.3-12-3.5-20.8-3.5-12.1 0-20.8 4.9-26.2 14.6s-8.1 22.6-8.1 38.7c0 29.2 9.4 43.8 28.1 43.8 7.9 0 14.4-2.3 19.5-7 4.9-4.9 7.5-10.4 7.5-16.6"/><path d="m1616.3 351.9c7.7 0 15.1 1.1 22.2 3.2v-27.3c0-4-2.3-6.1-7-6.5l-11.6-0.8v-21.4h50.3v164.3c0.2 4.1 2.4 6.2 6.8 6.2l9.5 0.5v21.6h-43.8v-15.7l-0.8-0.3c-8.1 13.2-20.4 19.7-36.8 19.7-20.5 0-35-6.8-43.2-20.5-7.6-12.4-11.4-27.7-11.4-45.7 0-23.4 5.8-42.2 17.3-56.2 11.5-14.1 27.7-21.1 48.5-21.1m22.1 97.9v-70c-6.5-2.9-13.3-4.3-20.5-4.3-11.9 0-20.6 4.8-26.2 14.3-5.4 9.6-8.1 21.7-8.1 36.5 0 30.3 9.7 45.4 29.2 45.4 7.4 0 13.5-2.1 18.4-6.2 4.8-4.4 7.2-9.6 7.2-15.7"/><path d="m1791.7 470.6s-12.5 4.7-19.2 4.7-9.2-3.3-9.2-11.8c0-3.8 0.5-8.8 1.4-14.9l10.2-63.1h32.6l2.8-17.7h-32.6l5.7-34.5-23.4 4.7-4.7 29.8-23.6 2.4-2.6 15.4h23.4l-10.5 65.4c-0.9 5.4-1.4 10.6-1.4 15.1 0 18.7 7.8 28.1 23.9 28.1 13.2 0 31-10.9 31-10.9l-3.8-12.7"/><path d="m1865 309.8-43.3 1.2-2.1 13 19.9 4.7-26 163.2h22.5l7.8-42.6s18.7-65 49.4-65c9.5 0 12.3 6.9 12.3 15.6 0 3.3-0.5 6.9-0.9 10.4l-13.5 81.6 43.3-2.4 2.1-13-19.9-3.5 10.6-66.2c0.7-5 1.2-9.7 1.2-14 0-17-6.9-28.6-25.8-28.6-35.9 0-54.9 45.6-55.8 48.2l18.2-102.6"/><path d="m2035 464.7s-21.5 10.6-38.8 10.6c-17.7 0-26-7.8-26-24.6 0-3.1 0.2-6.6 0.7-10.2 49 0 83-18.4 83-45.6 0-18.7-15.1-30.7-39-30.7-37.6 0-68.3 38.5-68.3 87.5 0 26 16.6 42.6 42.6 42.6 27.9 0 53-17.5 53-17.5l-7.2-12.1m-62-40.7c6.1-24.8 23.4-42.1 40.7-42.1 12.1 0 17.7 5 17.7 15.4 0.1 15.6-24.8 26.7-58.4 26.7"/><path d="m2093.7 491.9v-21.9l8.9-0.8c5.2-0.5 7.8-3.1 7.8-7.6v-125.6l-15.4-0.8v-23h74.1c26.5 0 47.1 7 61.9 21.1 15 14.1 22.4 34.9 22.4 62.4 0 17.1-2.3 32.1-6.8 44.9-4.5 12.6-10.6 22.5-18.4 29.7-15.5 14.4-34.8 21.6-57.8 21.6h-76.7m49.7-153.5v127.6h27.6c15.5 0 27.6-5.6 36.2-16.8s13-27.4 13-48.7c0-41.4-17.6-62.2-52.7-62.2h-24.1"/><path d="m2330 472.2c19.6 0 29.5-15.9 29.5-47.6 0-16-2.3-28.2-6.8-36.5-4.3-8.3-11.7-12.4-22.2-12.4-10.3 0-17.8 4-22.7 11.9s-7.3 18.7-7.3 32.4c0 25.4 4.7 41.4 14.1 47.8 4.2 2.9 9.3 4.4 15.4 4.4m-62.1-48.4c0-13.3 2-24.9 5.9-34.6 4-9.9 9.3-17.5 15.9-22.7 12.8-9.7 26.9-14.6 42.4-14.6 10.8 0 19.9 1.8 27.3 5.4 7.6 3.4 13.4 7.5 17.6 12.2 4.3 4.5 7.9 11.2 10.8 20 3.1 8.6 4.6 18.9 4.6 30.8 0 24.9-6 43.7-18.1 56.5s-27.6 19.2-46.5 19.2c-18.7 0-33.4-6-44.1-18.1-10.5-12.3-15.8-30.3-15.8-54.1"/><path d="m2438.2 422.5c0 15.3 2.9 27.2 8.6 35.7 5.8 8.5 14.1 12.7 24.9 12.7 11 0 21.8-3.9 32.4-11.6l11.6 20.8c-12.8 10.5-28.8 15.7-48.1 15.7s-34.5-6-45.7-18.1c-11-12.3-16.5-30.3-16.5-54.1s6.3-41.6 18.9-53.5c12.8-12.1 27.1-18.1 43-18.1 16 0 30.9 3.7 44.6 11.1v35.1l-24.9 1.9v-13c0-4.9-1.8-7.8-5.4-8.9-3.4-1.3-7-1.9-10.8-1.9-21.7-0.1-32.6 15.3-32.6 46.2"/><path d="m2592.9 376.5c-4.3-1.6-9.6-2.4-15.7-2.4s-11.1 1.4-14.9 4.3c-3.6 2.7-5.4 6.1-5.4 10.3 0 4 0.6 7.1 1.9 9.5 1.4 2.2 3.6 4.1 6.5 5.7 4.5 2.3 9.9 4.4 16.2 6.2 6.3 1.6 11 3 14.1 4.1 3.1 0.9 6.8 2.5 11.4 4.9 4.7 2.3 8.2 4.9 10.5 7.6 6.3 6.7 9.5 15.2 9.5 25.7 0 13.5-5 24.1-14.9 31.9-9.7 7.6-22.2 11.4-37.3 11.4-22 0-38.6-2.8-49.7-8.4v-37.6l24.3-1.9v13c0 7.9 7.6 11.9 22.7 11.9s22.7-5.5 22.7-16.5c0-4-1.4-7.2-4.1-9.7-2.5-2.5-5-4.2-7.6-5.1-2.5-0.9-5.6-1.8-9.2-2.7-3.4-0.9-6.8-1.8-10.3-2.7-3.2-0.9-6.8-2.1-10.8-3.5-3.8-1.6-8-3.9-12.7-6.8-9.2-5.9-13.8-15.9-13.8-29.7 0-14.1 5-24.9 14.9-32.4 9.9-7.6 22.3-11.4 37.3-11.4 15.1 0 30.1 3.6 44.9 10.8v32.4l-24.3 1.9v-11.4c0-4.7-2.1-7.8-6.2-9.4"/></g></svg>
			</a>
		</div>`;
    holder.appendChild(footer);

    // Build an element to hold any results message
    this.msg = {
      header: document.createElement("div"),
      footer: document.createElement("div"),
    };
    this.msg.header.classList.add("results-message", "results-header");
    this.msg.footer.classList.add("results-message", "results-footer");
    results.appendChild(this.msg.header);

    // Loop over projects and create any tabs that are needed
    for (let p = 0; p < this.projectorder.length; p++) {
      let slug = this.projectorder[p];
      if (!this.projects[slug].tab) {
        let tab = document.createElement("button");
        tab.innerHTML =
          (slug == config.all ? icons.book : icons.filter) +
          " " +
          this.projects[slug].name +
          '<span class="n"></span>';
        tab.id = "tab-" + slug;
        tab.classList.add("tab");
        tab.setAttribute("role", "tab");
        tab.setAttribute("aria-controls", "panel-" + slug);
        tab.setAttribute("tabindex", slug == config.all ? 0 : -1);
        tab.setAttribute("aria-selected", slug == config.all ? true : false);
        // Add a click/focus event
        tab.addEventListener("click", function (e) {
          e.preventDefault();
          e.stopPropagation();
          _obj.selectTab(e);
        });
        tab.addEventListener("focus", function (e) {
          e.preventDefault();
          e.stopPropagation();
          _obj.selectTab(e);
        });

        // Add keyboard navigation to arrow keys following https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/Tab_Role
        tab.addEventListener("keydown", function (e) {
          if (e.key == "ArrowDown" || e.key == "ArrowRight") {
            e.preventDefault();
            _obj.selectTab(e, 1);
          } else if (e.key == "ArrowUp" || e.key == "ArrowLeft") {
            e.preventDefault();
            _obj.selectTab(e, -1);
          }
        });
        tablist.appendChild(tab);
        let panel = document.createElement("div");
        panel.classList.add("panel");
        panel.setAttribute("role", "tabpanel");
        panel.setAttribute("aria-labelledby", "tab-" + slug);
        panel.style.display = slug == this.selectedPanel ? "" : "none";

        this.projects[slug].results = document.createElement("ul");
        this.projects[slug].results.classList.add("search");
        panel.appendChild(this.projects[slug].results);

        results.appendChild(panel);

        this.projects[slug].tab = tab;
        this.projects[slug].value = tab.querySelector(".n");
        this.projects[slug].panel = panel;
      }
    }

    results.appendChild(this.msg.footer);

    // Disable existing form behaviour
    form.addEventListener("submit", function (e) {
      e.preventDefault();
    });

    // Add keyup event to form input
    inp.addEventListener("keyup", function (e) {
      if (e.key == "ArrowDown") {
        _obj.navLi(e);
      } else {
        _obj.searchByString(e.target.value);
      }
    });

    // Function to search with an input string
    this.searchByString = function (str) {
      if (this.resultdelay) clearTimeout(this.resultdelay);
      if (str.length >= 2) {
        if (str in this.results) this.displayResults(str);
        else
          this.resultdelay = setTimeout(function () {
            _obj.getReadTheDocsResults(str);
          }, 500);
      } else {
        this.displayResults("");
      }
      return this;
    };

    this.getReadTheDocsResults = function (str, page) {
      // Set as loading
      form.classList.add("loading");

      let projstr = this.projectorder
        .join("+project:")
        .replace(new RegExp("^" + config.all + "[s+]"), "");
      let url;
      if (page) {
        url = (debug ? "https://corsproxy.io/?" : "") + page;
      } else {
        url =
          (debug ? "https://corsproxy.io/?https://readthedocs.org/" : "/_/") +
          ("api/v3/search/?q=" + projstr + "+" + encodeURIComponent(str));
      }
      console.info("Getting " + url);
      fetch(url, {})
        .then((response) => {
          return response.json();
        })
        .then((json) => {
          if (page) {
            _obj.results[str].next = json.next;
            _obj.results[str].results = _obj.results[str].results.concat(
              json.results,
            );
          } else {
            _obj.results[str] = json;
          }
          // Unset loading
          form.classList.remove("loading");
          _obj.displayResults(str);
        })
        .catch((e) => {
          // Unset loading
          form.classList.remove("loading");
          // Submit default form
          form.submit();
        });
      return this;
    };

    this.getMoreReadTheDocsResults = function () {
      let str = inp.value;
      let data = this.results[str];
      if (data.next)
        this.getReadTheDocsResults(str, data.next.replace(/%3A/g, ":"));
      return this;
    };

    this.formatResult = function (str, data) {
      let url = data.domain + data.path;
      let txt = '<a href="' + url + '" tabindex="-1">' + data.title + "</a>";
      let prevExtract = "";
      let extract;
      txt += " (from " + data.project.slug + ")";
      for (let b = 0; b < data.blocks.length; b++) {
        if (
          "highlights" in data.blocks[b] &&
          "content" in data.blocks[b].highlights &&
          data.blocks[b].highlights.content.length > 0
        ) {
          extract = data.blocks[b].highlights.content[0];

          // Sanitise HTML
          extract = extract.replace(/<span>(.*?)<\/span>/g, function (m, p1) {
            return "[[MATCH]]" + p1 + "[[/MATCH]]";
          });
          extract = extract.replace(/<[^\>]+>/g, "");
          extract = extract.replace(/\[\[(\/?)MATCH\]\]/g, function (m, p1) {
            return "<" + p1 + "strong>";
          });

          if (extract != prevExtract) txt += "<p>" + extract + "</p>";
          prevExtract = extract;
        }
      }
      return txt;
    };

    this.displayResults = function (str) {
      let data, slug, r, li, li2, result;
      if (str in this.results) {
        data = this.results[str];
      } else {
        data = { results: [] };
      }
      for (slug in this.projects) {
        this.projects[slug].count = 0;
        this.projects[slug].results.innerHTML = "";
      }

      // Get a count of how many results for each project
      for (r = 0; r < data.results.length; r++) {
        slug = data.results[r].project.slug;
        if (slug in this.projects) {
          this.projects[slug].count++;

          result = this.formatResult(str, data.results[r]);

          // Add result to appropriate panel list
          li = document.createElement("li");
          li.classList.add("kind-title");
          li.setAttribute("tabindex", 0);
          li.innerHTML = result;
          li.addEventListener("keyup", function (e) {
            _obj.navLi(e);
          });
          this.projects[slug].results.appendChild(li);

          li2 = document.createElement("li");
          li2.classList.add("kind-title");
          li2.setAttribute("tabindex", 0);
          li2.innerHTML = result;
          li2.addEventListener("keyup", function (e) {
            _obj.navLi(e);
          });
          this.projects[config.all].results.appendChild(li2);
        } else {
          console.warn("No " + slug + " in projects.", this.projects);
        }
      }

      // Hide any existing tabs
      for (slug in this.projects) {
        //this.projects[slug].value.innerHTML = (this.projects[slug].count > 0 ? ' (' + this.projects[slug].count + ')' : '(0)');
        this.projects[slug].value.innerHTML =
          " (" + this.projects[slug].count + ")";
        this.projects[slug].tab.style.display =
          this.projects[slug].count == 0 ? "none" : "";
      }

      // Update all tabs
      this.projects[config.all].tab.style.display =
        data.results.length > 0 ? "" : "none";
      this.projects[config.all].value.innerHTML =
        data.results.length > 0 ? " (" + data.results.length + ")" : "";

      // TO DO If the number of results is less than the count we create a "load more" link at the bottom
      if (data.next) {
        // Show a "load more results" link
        this.msg.footer.innerHTML =
          '<button class="load-more' +
          (config["load-more"].class ? " " + config["load-more"].class : "") +
          '">' +
          config["load-more"].label +
          "</button>";
        this.msg.footer
          .querySelector("button")
          .addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            _obj.getMoreReadTheDocsResults();
            return;
          });
      } else {
        this.msg.footer.innerHTML = "";
      }

      // Update the results message header
      this.msg.header.innerHTML =
        str && data.results.length == 0
          ? "<p" +
            (config["no-results"].class
              ? ' class="' + config["no-results"].class + '"'
              : "") +
            ">" +
            config["no-results"].label +
            "</p>"
          : "";

      return this;
    };

    this.selectTab = function (e, inc) {
      let tab =
        e.target.tagName.toUpperCase() === "BUTTON"
          ? e.target
          : e.target.closest("button");
      let found = "";
      // Find out which project this tab is
      for (var p = 0; p < this.projectorder.length; p++) {
        let slug = this.projectorder[p];
        if (this.projects[slug].tab == tab) found = slug;
      }
      // If we've been provided an increment we find the appropriate project
      if (typeof inc === "number") {
        let idx = this.projectorder.indexOf(found);
        let i = 0;
        do {
          idx =
            (idx + inc + this.projectorder.length) % this.projectorder.length;
          found = this.projectorder[idx];
          i++;
          // We try again if the tab is hidden and we haven't run out of projects (avoid an infinite loop)
        } while (
          this.projects[found].tab.style.display == "none" &&
          i < this.projectorder.length
        );
      }
      // Loop over projects setting the properties
      for (let p = 0; p < this.projectorder.length; p++) {
        let slug = this.projectorder[p];
        if (slug == found) {
          // Update the selected tab
          this.projects[slug].tab.setAttribute("aria-selected", "true");
          this.projects[slug].tab.setAttribute("tabindex", 0);
          this.projects[slug].tab.focus();
          this.projects[slug].panel.style.display = "";
          this.projects[slug].panel.removeAttribute("hidden");
        } else {
          // Deselect any others
          this.projects[slug].tab.removeAttribute("aria-selected");
          this.projects[slug].tab.setAttribute("tabindex", -1);
          this.projects[slug].panel.style.display = "none";
          this.projects[slug].panel.setAttribute("hidden", true);
        }
      }
      if (found in this.projects)
        this.projects[found].tab.scrollIntoView({
          behavior: "smooth",
          block: "center",
          inline: "nearest",
        });
      return this;
    };

    this.navLi = function (e) {
      var nextEl, prevEl;
      if (e.target == inp) {
        nextEl =
          this.projects[this.selectedPanel].results.querySelector(
            "li.kind-title",
          );
      } else {
        nextEl = next(e.target);
        prevEl = prev(e.target);
        if (!prevEl) prevEl = inp;
      }
      if (e.key == "ArrowDown") {
        if (nextEl) {
          nextEl.focus();
          nextEl.scrollIntoView({
            behavior: "smooth",
            block: "center",
            inline: "nearest",
          });
        }
      } else if (e.key == "ArrowUp") {
        if (prevEl) {
          prevEl.focus();
          prevEl.scrollIntoView({
            behavior: "smooth",
            block: "center",
            inline: "nearest",
          });
        }
      } else if (e.key == "Enter") {
        var a = e.target.querySelector("a");
        if (a) location.href = a.getAttribute("href");
      } else if (e.key == "Escape") {
        dialog.close();
      }
      return;
    };
    function next(el, selector) {
      const nextEl = el.nextElementSibling;
      if (!selector || (nextEl && nextEl.matches(selector))) return nextEl;
      return null;
    }
    function prev(el, selector) {
      const prevEl = el.previousElementSibling;
      if (!selector || (prevEl && prevEl.matches(selector))) return prevEl;
      return null;
    }
    function highlightAllMatches(text, search) {
      const regex = new RegExp(`(${search})`, "gi");
      return text.replace(regex, "<strong>$1</strong>");
    }
    return this;
  }

  ready(function () {
    let config = {};
    if (typeof set_search_config !== "undefined") config = set_search_config;
    let search = new Search(
      document.getElementById("pst-search-dialog"),
      config,
    );
  });
})(window || this);
