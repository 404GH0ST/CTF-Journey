package main

import "fmt"

func leftshift(value, shift int) int {
	retval := value
	for i := 0; i < shift; i++ {
		retval = retval << 1
	}
	return retval
}

func bitshift(value, shift int) int {
	if (value != 1) && (shift != 0) {
		if (value & 1 == 0) {
			value = bitshift(value>>1, shift-1)
		} else {
			new_val := leftshift(value, 3)
			value = bitshift(new_val+1, shift-1)
		}
	}
	return value
}

func main() {
	for i := 0; i <= 99999999; i++ {
		a := i + 68
		a = bitshift(a, 4)
		a = a + 68
		a = bitshift(a, 8) // a is 3978596937
		if a == 2650405211509321 {
			fmt.Printf("Found the magic number: %d\n", i)
      break
		} else {
			continue
		}
	}
}

