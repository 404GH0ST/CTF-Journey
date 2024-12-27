from itertools import product
import hashlib  # Import the modules

for x in range(0, 10):  # Iterate through the lengths
    for combo in product(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", repeat=x
    ):  # For each combination in this alphabet with this length
        result = hashlib.md5(
            ("f789bbc328a3d1a3" + "".join(combo)).encode("utf-8")
        ).hexdigest()  # Generate the result
        if (
            result.startswith("0e") and result[2:].isdigit()
        ):  # Check if result matches our requirements
            print(
                "f789bbc328a3d1a3" + "".join(combo)
            )  # If it does print out the string
        else:
            pass  # If not pass
