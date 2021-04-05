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

from pathlib import Path
from diff_match_patch import diff_match_patch

from bldr.cli import pass_environment, run_cmd

import click


@click.command("gen.up", short_help="Update Code Gen")
#@click.argument("path", required=False, type=click.Path(resolve_path=True))
@click.option("--regen", flag_value=True, help="Regenerate module templates")
@click.option("--reimport", flag_value=True, help="Re-import imported modules from their sources")
@click.option("--purge-local", flag_value=True, help='Purge local/local template.  Useful when re-importing "--as-template" templates')
@pass_environment
def cli(ctx, regen, reimport, purge_local):
    """Update Code Generation"""
    ctx.log(f"Updating Code Generation")

    # Render any templates to next

    if ctx.next_path.exists():
        bldr.util.rmtree(ctx.next_path)
    ctx.next_path.mkdir(parents=True, exist_ok=True)
    ctx.current_path.mkdir(parents=True, exist_ok=True)
    local_local_path = ctx.local_path / "local"
    if local_local_path.exists() and purge_local:
        bldr.util.rmtree(local_local_path)
        
    ctx.local_path.mkdir(parents=True, exist_ok=True)

    if regen:
        if ctx.prev_generated_path.exists():
            bldr.util.rmtree(ctx.prev_generated_path)

        if ctx.current_generated_path.exists():
            ctx.current_generated_path.rename(ctx.prev_generated_path)

        ctx.current_generated_path.mkdir(parents=True, exist_ok=True)
        ctx.gen_replay = True
        if 'generators' in ctx.env['gen']:
            generators = ctx.env['gen']['generators']
            for gen in generators:
                gen_type, *gen_args = gen
                if gen_type == 'gen':
                    subcommand, args = gen_args
                    bldr.gen.cmd(ctx, subcommand, args)
                elif gen_type == 'gen.import':
                    [generator_name, source, path, as_template] = gen_args
                    as_template = bool(as_template)
                    if reimport:
                        if Path(source).exists():
                            run_cmd(ctx, 'gen.import', source=source, path=path, as_template=as_template)
                        else:
                            ctx.log(f"Import source no longer exists: {source}")
                            bldr.gen.cmd(ctx, generator_name, None)
                    elif as_template == True:
                        ctx.log(f"Skipping top-level import from: {source}.  Use --reimport to reimport from its source")
                    else:
                        bldr.gen.cmd(ctx, gen[1], None)
        ctx.gen_replay = False

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

        if source_path == None:
            if os.path.exists(destination_path):
                self.ctx.vlog(f"Deleting {destination_path}")
                os.unlink(destination_path)
            # There is no source so we are done
            return True
                
        # if the destination does not exist, just copy the file
        if not os.path.exists(destination_path):
            self.ctx.vlog(f"Creating {destination_path}")
            shutil.copy(source_path, destination_path)
            return True

        try:
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
        except UnicodeDecodeError:
            self.ctx.vlog(f"Updating Binary {destination_path}")
            # This is a binary file so just copy from source to destination
            shutil.copy(source_path, destination_path)

        return True   

    def walk(self):
        bldr.gen.walk_triple(
            self.source_root_dir,
            self.previous_root_dir,
            self.destination_root_dir,
            self.render,
            self.filter_file,
            self.filter_dir)
            