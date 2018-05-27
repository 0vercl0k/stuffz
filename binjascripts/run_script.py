# @yrp604 & Axel '0vercl0k' Souchet - 12-May-2018
import binaryninja as bn

def run(bv):
    s = bn.interaction.get_open_filename_input('Please select a script to run')
    if not s: return
    env = globals()
    env['bv'] = bv
    execfile(s, env, env)

bn.PluginCommand.register(
    'Run script',
    "Expose 'run script' UI element",
    run
)
