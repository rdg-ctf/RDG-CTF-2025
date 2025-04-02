package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/pquerna/otp/totp"
)

type GenerateSecretResponse struct {
	Secret string `json:"secret"`
}

type VerifyOTPRequest struct {
	Secret string `json:"secret"`
	Token  string `json:"token"`
}

func generateSecretHandler(w http.ResponseWriter, r *http.Request) {

	key, err := totp.Generate(totp.GenerateOpts{
		Issuer:      "SecureApp",
		AccountName: "user@example.com",
	})
	if err != nil {
		log.Println("Error generating OTP secret:", err)
		http.Error(w, "Failed to generate OTP secret", http.StatusInternalServerError)
		return
	}

	secret := key.Secret()
	log.Printf("Generated OTP secret: %s", secret)

	token, err := totp.GenerateCode(secret, time.Now())
	if err != nil {
		log.Println("Error generating OTP token:", err)
		http.Error(w, "Failed to generate OTP token", http.StatusInternalServerError)
		return
	}
	log.Printf("Generated OTP token: %s", token)

	response := GenerateSecretResponse{
		Secret: secret,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func verifyOTPHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("Received request for /verify-otp")

	var req VerifyOTPRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		log.Println("Error decoding request:", err)
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	log.Printf("Verifying OTP: secret=%s, token=%s\n", req.Secret, req.Token)
	if req.Secret == "" || req.Token == "" {
		http.Error(w, "Missing secret or token", http.StatusBadRequest)
		return
	}

	valid := totp.Validate(req.Token, req.Secret)
	if !valid {
		http.Error(w, "Invalid OTP", http.StatusUnauthorized)
		return
	}

	w.WriteHeader(http.StatusOK)
	fmt.Fprintln(w, "OTP is valid")
}

func main() {
	http.HandleFunc("/generate-secret", generateSecretHandler)
	http.HandleFunc("/verify-otp", verifyOTPHandler)

	fmt.Println("2FA Microservice is running on :8080...")
	http.ListenAndServe(":8080", nil)
}
