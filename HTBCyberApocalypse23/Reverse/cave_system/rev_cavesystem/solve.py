import angr, sys

def main():
    binary_path = './cave'

    # Load binary into angr project
    project = angr.Project(binary_path)

    # Create initial state for simulation
    initial_state = project.factory.entry_state()

    # Create simulation manager
    sim_manager = project.factory.simgr(initial_state)

    # Define addresses to find and avoid

    target_addr = 0x401aba
    avoid_addr = 0x401ac8

    # Explore paths in the binary using angr
    sim_manager.explore(find=target_addr, avoid=avoid_addr)

    # Check if target was found
    if sim_manager.found:
        # Get first solution state
        solution_state = sim_manager.found[0]
        # Print input that led to solution state
        print(solution_state.posix.dumps(sys.stdin.fileno()))
    else:
        raise Exception("Could not find the solution")

if __name__ == "__main__":
    main()