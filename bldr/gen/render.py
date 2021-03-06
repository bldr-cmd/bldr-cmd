import os
import sys
import shutil
import runpy
import traceback

import jinja2

import bldr.gen
from bldr.environment import Environment

renderers = {}

def render_for(ext: str):
    def decorator(function):
        renderers[ext] = function
        return function
    return decorator

@render_for('bldr-pass')
def render_pass(template_data: dict, source_path: str, destination_path: str):
    shutil.copy(source_path, destination_path)

@render_for('bldr-j2')
def render_j2(template_data: dict, source_path: str, destination_path: str):
    if os.path.exists(destination_path + ".keep"):
        return

    # Do not render the .bldr-j2.ext.py file.  Its just a helper for the real template
    if source_path.endswith('.py') and os.path.exists(source_path[:-3]):
        return

    with open(source_path, 'r') as source_file:
        source_str = source_file.read()
    template = jinja2.Template(source_str)

    template_module = source_path + ".py"
    context = {}
    context.update(template_data)

    if os.path.exists(template_module):
        local_env = runpy.run_path(template_module, globals())
        context.update(local_env)

    outputText = template.render(context)

    with open(destination_path, 'w') as dest_file:
        dest_file.write(outputText)

@render_for('bldr-py')
def render_py(template_data: dict, source_path: str, destination_path: str):

    # hijack stdout long enough to render the file
    _prev_stdout = sys.stdout
    
    with open(destination_path, 'w') as dest_file:
        sys.stdout = dest_file
        try:
            
            context = {}
            context.update(template_data)
            runpy.run_path(source_path, globals())
        finally:
            sys.stdout = _prev_stdout


    return


def lookup_fx_ext(path: str):
    filename = os.path.basename(path)
    
    parts = filename.split(".")
    num_parts = len(parts)
    if num_parts < 2:
        return None

    parts.reverse()
    for part in parts:
        if part in renderers:
            renderext = part
            return (renderers[renderext], renderext)

    return None

def render(template_data: dict, source: str, destination: str, default_copy: bool = True):
    # Make sure we have resolved paths to strings at this point
    source = str(source)
    destination = str(destination)
    try:    
        # print(f"render {source} -> {destination}")
        fx_ext = lookup_fx_ext(source)
        if fx_ext != None:
            (render_fx, renderext) = fx_ext
            destination = destination.replace(f".{renderext}", '')
            render_fx(template_data, source, destination)
        else:
            # Default to copy the file over
            if default_copy:
                shutil.copy(source, destination)
    except:
        print(f"Error Rendering {source} -> {destination}")
        traceback.print_exc()

class CommonRender:
    def __init__(self, ctx: Environment, default_copy: bool):
        self.ctx = ctx
        self.template_data = ctx.env
        self.default_copy = default_copy
   
    def filter_file(self, _root: str, _file: str):
        return True

    def filter_dir(self, _root: str, _dir: str):
        return True

    def render(self, source: str, destination: str):
        pass

    def walk(self, template_root_dir: str, destination_root_dir: str):
        bldr.gen.walk_local(
            os.path.abspath(template_root_dir),
            os.path.abspath(destination_root_dir),
            self.render,
            self.filter_file,
            self.filter_dir)

class TemplateRender(CommonRender):
    def filter_file(self, _root: str, source: str):
        if lookup_fx_ext(source) != None:
            return True
        return self.default_copy

    def render(self, source: str, destination: str):
        return render(self.template_data, source, destination, self.default_copy)

class CommonTripleRender:
    def __init__(self, ctx: Environment, source_root_dir: str, previous_root_dir: str, destination_root_dir: str):
        self.ctx = ctx
        self.template_data = ctx.env
        self.source_root_dir = os.path.abspath(source_root_dir)
        self.previous_root_dir = os.path.abspath(previous_root_dir)
        self.destination_root_dir = os.path.abspath(destination_root_dir)

    def filter_file(self, _root: str, _file: str):
        return True

    def filter_dir(self, _root: str, _dir: str):
        return True

    def render(self, source_path: str, previous_path: str, destination_path: str):
        pass
        
    def walk(self):
        bldr.gen.walk_triple(
            self.source_root_dir,
            self.previous_root_dir,
            self.destination_root_dir,
            self.render,
            self.filter_file,
            self.filter_dir)

class CopyTemplatesRender(CommonRender):
    def render(self, source_path: str, destination_path: str):
        # if the destination does not exist, just copy the file
        self.ctx.vlog(f"Copying {source_path} -> {destination_path}")
        shutil.copy(source_path, destination_path)
        return True

class MoveTemplatesRender(CommonRender):
    def render(self, source_path: str, destination_path: str):
        # if the destination does not exist, just copy the file
        if 'bldr-' in os.path.basename(source_path):
            self.ctx.vlog(f"Moving {source_path} -> {destination_path}")
            shutil.move(source_path, destination_path)
            return True

def walk(ctx: Environment, template_root_dir: str, destination_root_dir: str, default_copy: bool = True):
    rend = TemplateRender(ctx, default_copy)
    rend.walk(template_root_dir, destination_root_dir)