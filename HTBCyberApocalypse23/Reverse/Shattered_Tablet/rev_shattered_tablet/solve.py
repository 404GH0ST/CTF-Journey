import angr

p = angr.Project('./tablet')
simgr = p.factory.simulation_manager(p.factory.entry_state())

simgr.explore(find=0x401359, avoid=0x401367)
for i in range(3):
    print(simgr.found[0].posix.dumps(i))
