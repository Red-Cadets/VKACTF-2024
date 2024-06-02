package main

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"log"
	"math/rand"
	"net"
	"time"

	"github.com/google/uuid"	
	_ "github.com/mattn/go-sqlite3"
	"google.golang.org/grpc"

	pb "gta-phrases-service/pb/gta_phrases_service"

	"golang.org/x/crypto/bcrypt"
)

var db *sql.DB

func initDB() {
	var err error
	db, err = sql.Open("sqlite3", "./db.sqlite3")
	if err != nil {
		log.Fatal(err)
	}
	_, err = db.Exec(`
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS phrases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            correct_answer TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS user_scores (
            user_id INTEGER REFERENCES users(id),
            score INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS sessions (
            user_id INTEGER REFERENCES users(id),
            token TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    `)
	if err != nil {
		log.Fatal(err)
	}
}

func hashPassword(password string) (string, error) {
	bytes, err := bcrypt.GenerateFromPassword([]byte(password), 14)
	if err != nil {
		return "", err
	}
	return string(bytes), nil
}

func checkPasswordHash(password, hash string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
	return err == nil
}

func generateToken() string {
	return uuid.New().String()
}

func register(ctx context.Context, req *pb.RegisterRequest) (*pb.RegisterResponse, error) {
	hashedPassword, err := hashPassword(req.Password)
	if err != nil {
		return nil, err
	}
	result, err := db.Exec("INSERT INTO users (username, password) VALUES (?,?)", req.Username, hashedPassword)
	if err != nil {
		return nil, err
	}
	lastInsertId, err := result.LastInsertId()
	if err != nil {
		return nil, err
	}
	_, err = db.Exec("INSERT INTO user_scores (user_id, score) VALUES (?,?)", lastInsertId, 0)
	if err != nil {
		return nil, err
	}
	return &pb.RegisterResponse{Success: lastInsertId > 0}, nil
}

func login(ctx context.Context, req *pb.LoginRequest) (*pb.LoginResponse, error) {
	var userID int64
	err := db.QueryRow("SELECT id FROM users WHERE username =?", req.Username).Scan(&userID)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, errors.New("no such user")
		}
		return nil, err
	}
	var authToken string
	err = db.QueryRow("SELECT token FROM sessions WHERE user_id =?", userID).Scan(&authToken)
	if err != nil && err != sql.ErrNoRows {
		return nil, err
	}
	if authToken == "" {
		authToken = generateToken()
		_, err = db.Exec("INSERT INTO sessions (user_id, token) VALUES (?, ?)", userID, authToken)
		if err != nil {
			return nil, err
		}
	}
	return &pb.LoginResponse{UserId: userID, AuthToken: authToken}, nil
}

func getUserIdFromToken(token string) (int64, error) {
	var userID int64
	err := db.QueryRow("SELECT user_id FROM sessions WHERE token =?", token).Scan(&userID)
	if err != nil {
		return 0, err
	}
	return userID, nil
}

func getPhrase(ctx context.Context, req *pb.GetPhraseRequest) (*pb.Phrase, error) {
	userID, err := getUserIdFromToken(req.AuthToken)
	if err != nil {
		return nil, errors.New("not logged in")
	}
	fmt.Println("UserID", userID)
	var phraseText string
	rows, err := db.Query("SELECT text FROM phrases")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var phrases []string
	for rows.Next() {
		var text string
		if err := rows.Scan(&text); err != nil {
			return nil, err
		}
		phrases = append(phrases, text)
	}

	if err = rows.Err(); err != nil {
		return nil, err
	}

	if len(phrases) == 0 {
		return nil, errors.New("no phrases found")
	}

	rand.Seed(time.Now().UnixNano())
	phraseText = phrases[rand.Intn(len(phrases))]

	return &pb.Phrase{Text: phraseText}, nil
}

func checkAnswer(ctx context.Context, req *pb.CheckAnswerRequest) (*pb.AnswerResult, error) {
	userID, err := getUserIdFromToken(req.AuthToken)
	if err != nil {
		return nil, errors.New("not logged in")
	}

	var correctAnswer string
	err = db.QueryRow("SELECT correct_answer FROM phrases WHERE text =?", req.Text).Scan(&correctAnswer)
	if err != nil {
		return nil, err
	}

	var scoreCount int
	err = db.QueryRow("SELECT COUNT(*) FROM user_scores WHERE user_id = ?", userID).Scan(&scoreCount)
	if err != nil {
		return nil, err
	}

	if scoreCount == 0 {

		_, err := db.Exec("INSERT INTO user_scores (user_id, score) VALUES (?, ?)", userID, 0)
		if err != nil {
			return nil, err
		}
	}

	var correctCount int32
	err = db.QueryRow("SELECT score FROM user_scores WHERE user_id = ?", userID).Scan(&correctCount)
	if err != nil {
		return nil, err
	}

	if req.Answer == correctAnswer {
		_, err = db.Exec("UPDATE user_scores SET score = score + 1 WHERE user_id = ?", userID)
		if err != nil {
			return nil, err
		}
		correctCount++
		if correctCount >= 100 {
			log.Printf("user %d win flag", userID)
			return &pb.AnswerResult{Correct: true, CorrectCount: correctCount, CorrectAnswer: correctAnswer, Flag: "vka{fake_flag}"}, nil
		}
		return &pb.AnswerResult{Correct: true, CorrectCount: correctCount, CorrectAnswer: correctAnswer, Flag: ""}, nil
	} else {
		_, err = db.Exec("UPDATE user_scores SET score = 0 WHERE user_id = ?", userID)
		if err != nil {
			return nil, err
		}
		return &pb.AnswerResult{Correct: false, CorrectCount: 0, CorrectAnswer: correctAnswer, Flag: ""}, nil
	}
}

func main() {
	initDB()
	lis, err := net.Listen("tcp", ":10049")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	server := &server{}
	pb.RegisterGTAGameServiceServer(s, server)
	log.Printf("server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}

type server struct{}

func (s *server) RegisterUser(ctx context.Context, req *pb.RegisterRequest) (*pb.RegisterResponse, error) {
	return register(ctx, req)
}

func (s *server) LoginUser(ctx context.Context, req *pb.LoginRequest) (*pb.LoginResponse, error) {
	return login(ctx, req)
}

func (s *server) GetPhrase(ctx context.Context, req *pb.GetPhraseRequest) (*pb.Phrase, error) {
	return getPhrase(ctx, req)
}

func (s *server) CheckAnswer(ctx context.Context, req *pb.CheckAnswerRequest) (*pb.AnswerResult, error) {
	return checkAnswer(ctx, req)
}
