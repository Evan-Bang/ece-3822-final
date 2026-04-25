#include "platform_sum.h"
#include <iostream>
#include <fstream>
#include <string>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

// Helper to read the port from your shared config file
int get_port_from_config(const std::string& key) {
    std::ifstream file("../../port_assignments.txt");
    std::string line;
    if (!file.is_open()) return 50074; // Default fallback

    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;
        if (line.find(key) == 0) {
            size_t pos = line.find('=');
            if (pos != std::string::npos) {
                return std::stoi(line.substr(pos + 1));
            }
        }
    }
    return 50074; 
}

void report_to_python(const std::string& game_name, const std::string& name, int score, long playtime) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        std::cerr << "[REPORTER ERROR] Socket creation failed\n";
        return;
    }

    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    
    int port = get_port_from_config("PLATFORM_SERVER");
    serv_addr.sin_port = htons(port);
    
    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
        std::cerr << "[REPORTER ERROR] Invalid address\n";
        close(sock);
        return;
    }

    if (connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
        std::cerr << "[REPORTER] Connection failed to Port " << port << "\n";
        close(sock);
        return;
    }

    std::string json_message = "{";
    json_message += "\"type\": \"game_summary\",";
    json_message += "\"game_name\": \"" + game_name + "\",";
    json_message += "\"username\": \"" + name + "\",";
    json_message += "\"score\": " + std::to_string(score) + ",";
    json_message += "\"playtime\": " + std::to_string(playtime);
    json_message += "}";

    send(sock, json_message.c_str(), json_message.length(), 0);
    
    std::cout << "[REPORTER] JSON Summary sent for " << name << " [" << game_name << "]\n";

    close(sock);
}