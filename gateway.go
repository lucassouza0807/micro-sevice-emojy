package main

import (
	"bufio"
	"fmt"
	"html/template"
	"io"
	"log"
	"net/http"
	"strings"

	"github.com/gorilla/mux"
)

var (
	templates      *template.Template
	streamedTextCh chan string
)

func init() {
	// Parse all templates in the templates folder.
	templates = template.Must(template.ParseGlob("templates/*.html"))
	streamedTextCh = make(chan string)
}

// generateText calls FastAPI and returns every token received on the fly through
// a dedicated channel (streamedTextCh).
func generateText(streamedTextCh chan<- string) {
	var buf io.Reader = nil

	req, err := http.NewRequest("GET", "http://127.0.0.1:8000", buf)
	if err != nil {
		log.Fatal(err)
	}

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	reader := bufio.NewReader(resp.Body)

	for {
		chunk, err := reader.ReadBytes('\x00')
		if err != nil {
			if err == io.EOF {
				break
			}
			log.Println(err)
			break
		}

		output := string(chunk)
		streamedTextCh <- output
	}
}

// formatServerSentEvent creates a proper SSE compatible body.
func formatServerSentEvent(event, data string) (string, error) {
	sb := strings.Builder{}

	_, err := sb.WriteString(fmt.Sprintf("event: %s\n", event))
	if err != nil {
		return "", err
	}
	_, err = sb.WriteString(fmt.Sprintf("data: %v\n\n", data))
	if err != nil {
		return "", err
	}

	return sb.String(), nil
}

// generate waits for new tokens and streams them as SSE.
func generate(w http.ResponseWriter, r *http.Request) {
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "SSE not supported", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/event-stream")

	for text := range streamedTextCh {
		event, err := formatServerSentEvent("streamed-text", text)
		if err != nil {
			http.Error(w, "Cannot format SSE message", http.StatusInternalServerError)
			return
		}

		_, err = fmt.Fprint(w, event)
		if err != nil {
			http.Error(w, "Cannot send SSE message", http.StatusInternalServerError)
			return
		}

		flusher.Flush()
	}
}

// start triggers text generation asynchronously.
func start(w http.ResponseWriter, r *http.Request) {
	go generateText(streamedTextCh)
	w.WriteHeader(http.StatusOK)
	fmt.Fprint(w, "Text generation started")
}

// home renders the home page.
func home(w http.ResponseWriter, r *http.Request) {
	if err := templates.ExecuteTemplate(w, "home.html", nil); err != nil {
		log.Println(err.Error())
		http.Error(w, "", http.StatusInternalServerError)
		return
	}
}

func main() {
	// Use gorilla/mux router
	r := mux.NewRouter()

	// Define routes
	r.HandleFunc("/generate", generate).Methods("GET")
	r.HandleFunc("/start", start).Methods("POST")
	r.HandleFunc("/", home).Methods("GET")

	// Start server
	log.Println("Server running on http://localhost:8000")
	log.Fatal(http.ListenAndServe(":8000", r))
}
