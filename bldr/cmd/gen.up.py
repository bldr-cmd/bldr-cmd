"""
`gen.up` Command

Regenerate Templates

"""
import os
import shutil

import bldr
import bldr.util
import bldr.gen
import bldr.gen.render

from diff_match_patch import diff_match_patch

from bldr.cli import pass_environment

import click


@click.command("gen.up", short_help="Update Code Gen")
#@click.argument("path", required=False, type=click.Path(resolve_path=True))
@click.argument("regen", required=False, type=click.BOOL)
@pass_environment
def cli(ctx, regen):
    """Update Code Generation"""
    ctx.log(f"Updating Code Generation")

    # Render any templates to next

    ctx.next_path.mkdir(parents=True, exist_ok=True)
    ctx.current_path.mkdir(parents=True, exist_ok=True)
    ctx.local_path.mkdir(parents=True, exist_ok=True)

    if regen:
        if ctx.prev_generated_path.exists():
            bldr.util.rmtree(ctx.prev_generated_path)

        # Generate to next_generated_path
        
        if ctx.current_generated_path.exists():
            ctx.current_generated_path.rename(ctx.prev_generated_path)

        ctx.next_generated_path.rename(ctx.current_generated_path)
    else:
        ctx.current_generated_path.mkdir(parents=True, exist_ok=True)

    bldr.gen.render.walk(ctx, ctx.current_generated_path, ctx.next_path, True)
    bldr.gen.render.walk(ctx, ctx.local_path, ctx.next_path, True)
    bldr.gen.render.walk(ctx, ctx.proj_path, ctx.next_path, False)
    
    # Diff + Patch
    diff_patch_render = DiffPatchRender(ctx, ctx.next_path, ctx.current_path, ctx.proj_path) 
    diff_patch_render.walk()

    if ctx.prev_path.exists():
        bldr.util.rmtree(ctx.prev_path)
    ctx.current_path.rename(ctx.prev_path)
    ctx.next_path.rename(ctx.current_path)
    ctx.next_path.mkdir()


class DiffPatchRender(bldr.gen.render.CommonTripleRender):
    def __init__(self, ctx: dict, source_root_dir: str, previous_root_dir: str, destination_root_dir: str):
        bldr.gen.render.CommonTripleRender.__init__(self, ctx, source_root_dir, previous_root_dir, destination_root_dir)
        self.dmp = diff_match_patch()
   
    def render(self, source_path: str, previous_path: str, destination_path: str):
        # if the destination does not exist, just copy the file
        if not os.path.exists(destination_path):
            self.ctx.vlog(f"Creating {destination_path}")
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
            self.ctx.vlog(f"Current {destination_path}")
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
            