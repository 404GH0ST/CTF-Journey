package main

import (
  "fmt"
  "math"
)

func main(){
  p := 0xdd6cc28d
  A := 0xcfabb6dd
  _ = 0xc4a21ba9
  g := 0x83e21c05
  
  for i := 0; i <= p; i++ {
    new_A := int(math.Pow(float64(g), float64(i))) % p
    fmt.Printf("New_A is : %v\n", new_A)
    if new_A == A{
      fmt.Printf("Found a : %v\n", i)
      break
    }
  }
}
