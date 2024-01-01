import z3

known_numbers = [102, 108, 97, 103, 123] # Each byte representation of "flag{"
last_number = [125] # Byte representation of "}"
numbers = [z3.Int(f'n{i}') for i in range(6)]

current_sum = sum(known_numbers)
current_sum += last_number[0]

solver = z3.Solver()

solver.add(z3.Sum(numbers) == 1337 - current_sum)

for n in numbers: 
    solver.add(z3.And(n >= 95, n <= 122))
    
if solver.check() == z3.sat: 
    # Get the solution 
    model = solver.model() 
    
    guessed_numbers = [model[n].as_long() for n in numbers]
    
    full_numbers = known_numbers + guessed_numbers + last_number
    
    flag = "".join([chr(n) for n in full_numbers])
    
    print(f"Flag: {flag}")
    
else: 
    # No solution exists 
    print("No solution")