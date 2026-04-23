/*
player.cpp - Player implementation with switchable buffering strategy
Including Score and Playtime tracking.
*/

#include "player.h"
#include <sys/time.h>
#include <iostream>
#include <ctime> // For std::time

// Helper to get current timestamp in milliseconds
static long get_timestamp_ms() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec * 1000 + tv.tv_usec / 1000;
}

// Default constructor
Player::Player() {
    id = 0;
    name = "";
    x = 400.0;
    y = 300.0;
    socket = -1;
    connected = false;
    character_type = "";
    status = "down";
    
    // SCORE AND TIME LOGIC FOR LEADERBOARDS
    score = 0;
    join_time = std::time(nullptr);
   
    #ifdef USE_POSITION_SMOOTHER
        buffer = new PositionSmoother(5);
        std::cout << "[BUFFER] Using PositionSmoother (low latency)\n";
    #else
        buffer = new JitterBuffer(10, 3);
        std::cout << "[BUFFER] Using JitterBuffer (high smoothness)\n";
    #endif
}

// Parameterized constructor
Player::Player(int id, std::string name, float x, float y, int socket) {
    this->id = id;
    this->name = name;
    this->x = x;
    this->y = y;
    this->socket = socket;
    this->connected = true;
    this->character_type = "";
    this->status = "down";
    
    //NEW STATS INITIALIZATION 
    this->score = 0;
    this->join_time = std::time(nullptr); 

    
    #ifdef USE_POSITION_SMOOTHER
        buffer = new PositionSmoother(5);
        std::cout << "[BUFFER] Player " << id << " using PositionSmoother\n";
    #else
        buffer = new JitterBuffer(10, 3);
        std::cout << "[BUFFER] Player " << id << " using JitterBuffer\n";
    #endif
    
    buffer->add_position(x, y, get_timestamp_ms());
}

// Destructor
Player::~Player() {
    delete buffer;
}


int Player::get_score() const { 
    return score; 
}

long Player::get_playtime() const { 
    // Returns difference between "now" and "join time" in seconds
    return (long)(std::time(nullptr) - join_time); 
}

void Player::add_score(int points) { 
    score += points; 
}

void Player::set_score(int new_score) { 
    score = new_score; 
}


int Player::get_id() const { return id; }
std::string Player::get_name() const { return name; }
float Player::get_x() const { return x; }
float Player::get_y() const { return y; }
int Player::get_socket() const { return socket; }
bool Player::is_connected() const { return connected; }
std::string Player::get_character_type() const { return character_type; }
std::string Player::get_status() const { return status; }

// --- SETTERS ---
void Player::set_position(float new_x, float new_y) {
    x = new_x;
    y = new_y;
}

void Player::set_name(std::string new_name) {
    name = new_name;
}

void Player::set_connected(bool status) {
    connected = status;
}

void Player::set_socket(int sock) {
    socket = sock;
}

void Player::set_character_type(std::string type) {
    character_type = type;
}

void Player::set_status(std::string new_status) {
    status = new_status;
}

// Buffer management methods
void Player::add_raw_position(float new_x, float new_y) {
    buffer->add_position(new_x, new_y, get_timestamp_ms());
}

Position Player::get_smoothed_position() {
    try {
        #ifdef USE_POSITION_SMOOTHER
            return buffer->get_exponential_smooth(0.9f);
        #else
            if (buffer->is_ready()) {
                return buffer->get_current_position();
            } else {
                return Position(x, y);
            }
        #endif
    } catch (...) {
        return Position(x, y);
    }
}

bool Player::operator==(const Player& other) const {
    return id == other.id;
}