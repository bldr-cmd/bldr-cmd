"""
`gen.up` Command

Regenerate Templates

"""
import os
import shutil

import bldr
import bldr.gen
import bldr.gen.render

from diff_match_patch import diff_match_patch

from bldr.cli import pass_environment

import click

# aliases
join = os.path.join

@click.command("gen.up", short_help="Update Code Gen")
#@click.argument("path", required=False, type=click.Path(resolve_path=True))
@pass_environment
def cli(ctx):
    """Update Code Generation"""
    ctx.log(f"Updating Code Generation")

    dotbldr_path = bldr.dotbldr_path()
    proj_path = bldr.proj_path()

    # Render any templates to next
    next_path = join(dotbldr_path, "next")
    prev_path = join(dotbldr_path, "current")
    old_prev_path = join(dotbldr_path, "current.old")
    local_path = join(dotbldr_path, "local")
    template_path = join(dotbldr_path, "template")

    bldr.ensure_dir(next_path)
    bldr.ensure_dir(prev_path)
    bldr.ensure_dir(local_path)
    bldr.ensure_dir(template_path)

    bldr.gen.render.walk(ctx, template_path, next_path, False)
    bldr.gen.render.walk(ctx, local_path, next_path, False)
    bldr.gen.render.walk(ctx, proj_path, next_path, False)
    
    # Diff + Patch
    diff_patch_render = DiffPatchRender(ctx, next_path, prev_path, proj_path) 
    diff_patch_render.walk()

    if os.path.exists(old_prev_path):
        shutil.rmtree(old_prev_path)
    os.rename(prev_path, old_prev_path)
    os.rename(next_path, prev_path)
    os.makedirs(next_path)


class DiffPatchRender(bldr.gen.render.CommonTripleRender):
    def __init__(self, ctx: dict, source_root_dir: str, previous_root_dir: str, destination_root_dir: str):
        bldr.gen.render.CommonTripleRender.__init__(self, ctx, source_root_dir, previous_root_dir, destination_root_dir)
        self.dmp = diff_match_patch()
   
    def render(self, source_path: str, previous_path: str, destination_path: str):
        # if the destination does not exist, just copy the file
        if not os.path.exists(destination_path):
            self.ctx.log(f"Creating {destination_path}")
            shutil.copy(source_path, destination_path)
            return True

        source_text = ''
        if os.path.exists(source_path):
            with open(source_path, 'r') as source_file:
                source_text = source_file.read()

        previous_text = ''
        if os.path.exists(previous_path):
            with open(previous_path, 'r') as previous_file:
                previous_text = previous_file.read()

        patches = self.dmp.patch_make(previous_text, source_text)

        if len(patches) == 0:
            self.ctx.log(f"Current {destination_path}")
            return False

        self.ctx.log(f"Updating {destination_path}")
        destination_text = ''
        with open(destination_path, 'r') as destination_file:
            destination_text = destination_file.read()
        
        (destination_text, _success_list) = self.dmp.patch_apply(patches, destination_text)

        with open(destination_path, 'w') as destination_file:
            destination_file.write(destination_text)
        return True   

    def walk(self):
        bldr.gen.walk_triple(
            self.source_root_dir,
            self.previous_root_dir,
            self.destination_root_dir,
            self.render,
            self.filter_file,
            self.filter_dir)
            