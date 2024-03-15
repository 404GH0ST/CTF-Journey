package main

import (
	"fmt"
	"math/big"
)

func main() {
	pHex := "397"
	AHex := "2c2"
	// BHex := "c4a21ba9"
	gHex := "1c3"

	p := new(big.Int)
	p.SetString(pHex, 16)

	A := new(big.Int)
	A.SetString(AHex, 16)

	g := new(big.Int)
	g.SetString(gHex, 16)

	fmt.Println("Testing:")

	for i := new(big.Int); i.Cmp(p) <= 0; i.Add(i, big.NewInt(1)) {
		newA := new(big.Int).Exp(g, i, p)
		if newA.Cmp(A) == 0 {
			fmt.Printf("Found a: %s\n", i.Text(10))
			break
		}
	}
}

