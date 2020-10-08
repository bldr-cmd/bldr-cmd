import os
import shutil
import runpy

import jinja2

import bldr.gen

renderers = {}

def render_for(ext: str):
    def decorator(function):
        renderers[ext] = function
        return function
    return decorator

@render_for('bldr-j2')
def render_j2(template_data: dict, source_path: str, destination_path: str):
    if os.path.exists(destination_path + ".keep"):
        return

    with open(source_path, 'r') as source_file:
        source_str = source_file.read()
    template = jinja2.Template(source_str)

    template_module = source_path.replace("bldr-j2", "bldr-py") 
    context = {}
    context.update(template_data)

    if os.path.exists(template_module):
        local_env = runpy.run_path(template_module, globals())
        context.update(local_env)

    outputText = template.render(context)

    with open(destination_path, 'w') as dest_file:
        dest_file.write(outputText)

def render(template_data: dict, source: str, destination: str, default_copy: bool):
    filename = os.path.basename(source)
    
    parts = filename.split(".")
    renderext = parts[-2]
    destination = destination.replace("." + renderext, '')
    # print(f"render {source} -> {destination}")

    if renderext in renderers:
        renderers[renderext](template_data, source, destination)
    else:
        # Default to copy the file over
        if default_copy:
            shutil.copy(source, destination)

class TemplateRender:
    def __init__(self, template_data: dict, default_copy: bool):
        self.template_data = template_data
        self.default_copy = default_copy
   
    def filter_file(self, _root: str, _file: str):
        return True

    def filter_dir(self, _root: str, _dir: str):
        return True

    def render(self, source: str, destination: str):
        return render(self.template_data, source, destination, self.default_copy)

    def walk(self, template_root_dir: str, destination_root_dir: str):
        bldr.gen.walk_local(
            os.path.abspath(template_root_dir),
            os.path.abspath(destination_root_dir),
            self.render,
            self.filter_file,
            self.filter_dir)

def walk(template_data: dict, template_root_dir: str, destination_root_dir: str, default_copy: bool = True):
    rend = TemplateRender(template_data, default_copy)
    rend.walk(template_root_dir, destination_root_dir)