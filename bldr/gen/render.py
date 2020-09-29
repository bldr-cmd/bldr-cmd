import os
import shutil

import jinja2

import bldr.gen

renderers = {}

def render_for(ext: str):
    def decorator(function):
        return function
    renderers[ext] = decorator
    return decorator

@render_for('bldr-j2')
def render_j2(template_data: dict, source_path: str, destination_path: str):
    if os.path.exists(destination_path + ".keep"):
        return

    with open(source_path, 'r') as source_file:
        source_str = source_file.read().decode('utf-8')
    template = jinja2.Template(source_str)

    template_module = source_path.replace("bldr-j2", "bldr-py") 

    if os.path.exists(template_module):
        with open(template_module, 'r') as source_module: 
            exec(source_module.read().decode('utf-8'), globals(), template_data)

    outputText = template.render(template_data)

    with open(destination_path, 'w') as dest_file:
        dest_file.write(outputText)

def render(template_data: dict, source: str, destination: str):
    filename = os.path.basename(source)

    parts = filename.split(".")
    renderext = parts[-2]

    if renderext in renderers:
        renderers[renderext](template_data, source, destination)
    else:
        # Default to copy the file over
        shutil.copy(source, destination)

class TemplateRender:
    def __init__(self, template_data: dict):
        self.template_data = template_data
   
    def filter_file(self, _root: str, _file: str):
        return True

    def filter_dir(self, _root: str, _dir: str):
        return True

    def render(self, source: str, destination: str):
        return render(self.template_data, source, destination)

    def walk(self, template_root_dir: str, source_root_dir: str):
        bldr.gen.walk_local(
            template_root_dir,
            source_root_dir,
            self.render,
            self.filter_file,
            self.filter_dir)

def walk(template_data: dict, template_root_dir: str, source_root_dir: str):
    rend = TemplateRender(template_data)
    rend.walk(template_root_dir, source_root_dir)