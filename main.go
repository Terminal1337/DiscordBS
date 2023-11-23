package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/tidwall/gjson"
)

var (
	client *http.Client
)

func readLinesFromFile(filePath string) ([]string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return lines, nil
}
func sendDM(token string, count int, message string, userID string) {
	payload := fmt.Sprintf(`{"recipient_id": "%s"}`, userID)

	request, err := http.NewRequest("POST", "https://canary.discord.com/api/v9/users/@me/channels", strings.NewReader(payload))
	if err != nil {
		log.Fatalln(err.Error())
	}

	request.Header.Set("Authorization", fmt.Sprintf("Bot %s", token))
	request.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(request)
	if err != nil {
		log.Fatalln(err.Error())
	}
	defer resp.Body.Close()

	b, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err.Error())
	}
	channelID := gjson.Get(string(b), "id").String()
	payload = fmt.Sprintf(`{"content": "%s"}`, message)

	for i := 0; i < count; i++ {
		time.Sleep(300 * time.Millisecond)
		request, err = http.NewRequest("POST", fmt.Sprintf("https://canary.discord.com/api/v9/channels/%s/messages", channelID), strings.NewReader(payload))
		if err != nil {
			continue
		}
		request.Header.Set("Authorization", fmt.Sprintf("Bot %s", token))
		request.Header.Set("Content-Type", "application/json")

		response, err := client.Do(request)
		if err != nil {
			continue
		}
		defer response.Body.Close()
		fmt.Println(response.StatusCode)

	}

}
func MustParseURL(urlStr string) *url.URL {
	parsedURL, err := url.Parse(urlStr)
	if err != nil {
		panic(err)
	}
	return parsedURL
}
func main() {
	tokenslist, err := readLinesFromFile("tokens.txt")
	if err != nil {
		log.Fatalln(err.Error())
	}
	proxyURL := "http://sePiXSQgL:WZddrQgSQpEKeMERl@delta.proxies.cx:47212"
	transport := &http.Transport{
		Proxy: http.ProxyURL(MustParseURL(proxyURL)),
	}
	client = &http.Client{Transport: transport}
	app := fiber.New()
	app.Get("/api/spam", func(c *fiber.Ctx) error {
		if c.Query("userid") == "" || c.Query("limit") == "" || c.Query("message") == "" {
			return c.SendString("Invalid Parameters")
		}
		userID := c.Query("userid")
		message := c.Query("message")
		limitStr := c.Query("limit")
		limit, err := strconv.Atoi(limitStr)
		if err != nil {
			return c.SendString("Invalid limit parameter")
		}
		for _, token := range tokenslist {
			go sendDM(token, limit, message, userID)

		}
		c.SendStatus(204)
		return c.SendString(fmt.Sprintf("Sent %d messages to %s", limit, userID))
	})

	app.Listen(":3000")

}
