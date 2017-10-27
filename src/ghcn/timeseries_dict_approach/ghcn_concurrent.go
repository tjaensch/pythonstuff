package main

import (
    "bufio"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	//"sync"
	"time"
)

var stationIdsSlice []string = getStationIdsSlice()

// Generic error checking function
func checkError(reason string, err error) {
	if err != nil {
		fmt.Printf("%s: %s\n", reason, err)
		os.Exit(1)
	}
}

func main() {
	log.Printf("Working digging up files...")
	t0 := time.Now()

    getStationInfo()

    ghcn("AGE00147710")

    /*for _, stationId := range stationIds {
    	ghcn(stationId)
    }*/

    /*var wg sync.WaitGroup

	// Start goroutine for each files segment of ncFiles slice
	fileSegments := getFileSegments()
	for _, fileSegment := range fileSegments {
		wg.Add(1)
		go func(fileSegment []string) {
			defer wg.Done()
			for _, stationId := range fileSegment {
				ghcn(stationId)
			}
		}(fileSegment)
	}

	// Wait until all goroutines finish
	wg.Wait()*/
    
    cleanUp()

    t1 := time.Now()
	log.Printf("The program took %v hours to run.\n", t1.Sub(t0).Hours())
}

// Create fileSegments slice of slice for concurrent processing
/*func getFileSegments() [][]string {
	// Create a slice of ncFiles
	fileSegments := make([][]string, 0)
	// Determine the length of the subslices based on amount of files and how many files can be open at the same time in PuTTY
	increaseRate := 2000
	// Add subslices to fileSegments slice
	for i := 0; i < len(stationIdsSlice)-increaseRate; i += increaseRate {
		fileSegments = append(fileSegments, stationIdsSlice[i:i+increaseRate])
	}
	fileSegments = append(fileSegments, stationIdsSlice[len(stationIdsSlice)-increaseRate:])
	return fileSegments
}*/

func getStationInfo() {
	cmdArgs := []string{"get_station_info.py"}
	if _, err := exec.Command("python", cmdArgs...).Output(); err != nil {
		checkError("Something went wrong with executing get_station_info.py, program exiting.", err)
	}
}

func getStationIdsSlice() []string {
	out, _ := os.Create("ghcn_stations.txt")
	defer out.Close()
	resp, _ := http.Get("https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt")
	defer resp.Body.Close()
	io.Copy(out, resp.Body)
	var stationIds []string
	file, err := os.Open("ghcn_stations.txt")
	checkError("Something went wrong with opening ghcn_stations.txt, program exiting.", err)
	defer file.Close()
	fileScanner := bufio.NewScanner(file)
	for fileScanner.Scan() {
		stationIds = append(stationIds, fileScanner.Text()[0:11])
	}
	//fmt.Print(stationIds)
	return stationIds
}

func ghcn(stationId string) {
	cmdArgs := []string{"ghcn.py", stationId}
	if _, err := exec.Command("python", cmdArgs...).Output(); err != nil {
		checkError("Something went wrong with executing ghcn.py, program exiting.", err)
	}
	fmt.Println(stationId)
}

func cleanUp() {
	os.Remove("stationIds.npy")
	os.Remove("latDict.npy")
	os.Remove("lonDict.npy")
	os.Remove("elevationDict.npy")
	os.Remove("stationLongNameDict.npy")
	os.Remove("ghcn_stations.txt")
}
