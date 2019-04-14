from jinja2 import Environment, PackageLoader, meta

import jinja2schema

env = Environment(loader=PackageLoader("sunpy_sphinx_theme", "sunpy"))
template_source = env.loader.get_source(env, "docsidebar.html")[0]
parsed_content = env.parse(template_source)
meta.find_undeclared_variables(parsed_content)
abc = jinja2schema.infer(template_source)
