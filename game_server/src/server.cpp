/*
server.cpp - Game server with polymorphic serialization and chat filtering

Compile with different serializers:
  make SERIALIZER=TEXT    (default)
  make SERIALIZER=JSON
  make SERIALIZER=BINARY

Run:
  ./server_text --name MyGame --port 8080
*/

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <cstring>
#include <cstdlib>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <algorithm>

#include "player.h"
#include "serializer.h"
#include "text_serializer.h"
#include "json_serializer.h"
#include "binary_serializer.h"
#include "platform_sum.h"
#include "bloom_filter.h"

#ifdef USE_JSON
    #define SERIALIZER_TYPE JSONSerializer
#elif defined(USE_BINARY)
    #define SERIALIZER_TYPE BinarySerializer
#else
    #define SERIALIZER_TYPE TextSerializer
#endif

class GameServer {
private:
    int server_socket;
    std::map<int, Player*> players;
    Serializer* serializer;
    int next_player_id = 1;
    int port;
    std::string game_name;
    std::string chat_file;
    std::string blocked_words_file;
    BloomFilter bf;

public:
    GameServer(int port, std::string name) : port(port), game_name(name), bf(33165, 10) {
        serializer = new SERIALIZER_TYPE();

        server_socket = socket(AF_INET, SOCK_STREAM, 0);
        if (server_socket < 0) {
            std::cerr << "Failed to create socket\n";
            exit(1);
        }

        int opt = 1;
        setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

        struct sockaddr_in address;
        address.sin_family = AF_INET;
        address.sin_addr.s_addr = INADDR_ANY;
        address.sin_port = htons(port);

        if (bind(server_socket, (struct sockaddr*)&address, sizeof(address)) < 0) {
            std::cerr << "Failed to bind to port " << port << "\n";
            std::cerr << "Error: " << strerror(errno) << "\n";
            exit(1);
        }

        if (listen(server_socket, 10) < 0) {
            std::cerr << "Failed to listen\n";
            exit(1);
        }

        // Set non-blocking BEFORE we start accepting
        fcntl(server_socket, F_SETFL, O_NONBLOCK);

        chat_file = game_name + "_chat_history.txt";
        blocked_words_file = "blocked_words.txt";

        std::ifstream file(blocked_words_file);
        if (file.is_open()) {
            std::string bline;
            while (std::getline(file, bline)) {
                if (!bline.empty()) {
                    bline.erase(bline.find_last_not_of(" \n\r\t") + 1);
                    bf.add_word(bline);
                }
            }
            file.close();
        }

        std::cout << "======================================\n";
        std::cout << "Game Server Started\n";
        std::cout << "======================================\n";
        std::cout << "Game:       " << game_name << "\n";
        std::cout << "Port:       " << port << "\n";
        std::cout << "Serializer: " << serializer->getName() << "\n";
        std::cout << "======================================\n";
    }

    ~GameServer() {
        for (auto& pair : players) delete pair.second;
        delete serializer;
        close(server_socket);
    }

    std::string process_message(const std::string& message) {
        std::stringstream ss(message);
        std::string word, result;
        bool first = true;
        while (ss >> word) {
            if (!first) result += " ";
            first = false;
            std::string clean = word;
            std::transform(clean.begin(), clean.end(), clean.begin(), ::tolower);
            clean.erase(std::remove_if(clean.begin(), clean.end(), ::ispunct), clean.end());

            if (bf.check_word(clean)) result += "***";
            else result += word;
        }
        return result;
    }

    void parse_update(Player* p, const std::string& line) {
        std::istringstream ss(line);
        std::string type, id_str, x_str, y_str, name, char_type, status, score_str;
        std::getline(ss, type, '|');
        std::getline(ss, id_str, '|');
        std::getline(ss, x_str, '|');
        std::getline(ss, y_str, '|');
        std::getline(ss, name, '|');
        std::getline(ss, char_type, '|');
        std::getline(ss, status, '|');
        std::getline(ss, score_str);

        if (!x_str.empty() && !y_str.empty()) {
            try {
                p->add_raw_position(std::stof(x_str), std::stof(y_str));
                Position smoothed = p->get_smoothed_position();
                p->set_position(smoothed.x, smoothed.y);
            } catch (...) {}
        }
        if (!name.empty()) p->set_name(name);
        if (!char_type.empty()) p->set_character_type(char_type);
        if (!status.empty()) p->set_status(status);
        if (!score_str.empty()) {
            try { p->set_score(std::stoi(score_str)); } catch (...) {}
        }
    }

    void handle_chat(int sender_id, const std::string& line) {
        std::stringstream ss(line);
        std::string type, name, content;
        std::getline(ss, type, '|');
        std::getline(ss, name, '|');
        std::getline(ss, content);

        if (content.empty()) return;

        std::string filtered = process_message(content);
        std::string final_msg = "CHAT|" + name + "|" + filtered;

        // Save filtered message to history
        std::ofstream outfile(chat_file, std::ios::app);
        if (outfile.is_open()) {
            outfile << final_msg << "\n";
            outfile.close();
        }

        // Broadcast to ALL players including the sender so they see the
        // filtered version echoed back (fixes client "not enough values" error
        // caused by the sender never receiving their own message)
        std::string packet = final_msg + "\n";
        for (auto& [id, p] : players) {
            send(p->get_socket(), packet.c_str(), packet.size(), 0);
        }
    }

    void accept_connections() {
        struct sockaddr_in client_addr;
        socklen_t addr_len = sizeof(client_addr);
        int client_socket = accept(server_socket, (struct sockaddr*)&client_addr, &addr_len);

        if (client_socket >= 0) {
            fcntl(client_socket, F_SETFL, O_NONBLOCK);

            int player_id = next_player_id++;
            players[player_id] = new Player(player_id, "Player" + std::to_string(player_id), 400, 300, client_socket);

            // Send connection confirmation
            std::string welcome = "CONNECTED|" + std::to_string(player_id) + "\n";
            send(client_socket, welcome.c_str(), welcome.length(), 0);

            // Replay chat history — only send lines with the correct
            // CHAT|name|content format (3 fields) so old 2-field entries
            // from a previous server version don't break the client
            std::ifstream history_file(chat_file);
            if (history_file.is_open()) {
                std::string h_line;
                while (std::getline(history_file, h_line)) {
                    if (h_line.empty()) continue;

                    // Count pipe separators: need at least 2 (3 fields)
                    int pipes = 0;
                    for (char c : h_line) if (c == '|') pipes++;

                    if (pipes >= 2) {
                        std::string msg = h_line + "\n";
                        send(client_socket, msg.c_str(), msg.size(), 0);
                    }
                }
                history_file.close();
            }

            std::cout << "[PLAYER " << player_id << "] Connected and history sent.\n";
        }
    }

    void receive_messages() {
        std::vector<int> disconnected;

        for (auto& [id, p] : players) {
            char buffer[4096];
            int n = recv(p->get_socket(), buffer, sizeof(buffer) - 1, 0);

            if (n > 0) {
                buffer[n] = '\0';
                std::istringstream stream(buffer);
                std::string line;
                while (std::getline(stream, line)) {
                    if (line.empty()) continue;
                    if (line.substr(0, 6) == "UPDATE") parse_update(p, line);
                    else if (line.substr(0, 4) == "CHAT") handle_chat(p->get_id(), line);
                }
            } else if (n == 0 || (n < 0 && errno != EAGAIN && errno != EWOULDBLOCK)) {
                disconnected.push_back(p->get_id());
            }
        }

        for (int id : disconnected) {
            Player* p = players[id];

            std::cout << "\n" << std::string(30, '-') << "\n";
            std::cout << "[DISCONNECT] Player Summary\n";
            std::cout << "  Name:     " << p->get_name() << "\n";
            std::cout << "  ID:       " << p->get_id() << "\n";
            std::cout << "  Score:    " << p->get_score() << "\n";

            long total_seconds = p->get_playtime();
            int minutes = total_seconds / 60;
            int seconds = total_seconds % 60;
            std::cout << "  Playtime: " << minutes << "m " << seconds << "s\n";
            std::cout << std::string(30, '-') << "\n\n";

            // Report to platform server (separate from game clients)
            report_to_python(game_name, p->get_name(), p->get_score(), p->get_playtime());

            close(p->get_socket());
            delete p;
            players.erase(id);
        }
    }

    void broadcast_state() {
        if (players.empty()) return;

        std::ostringstream state;
        state << "STATE";
        for (auto& pair : players) {
            state << "||" << serializer->serialize(*pair.second);
        }
        state << "\n";

        std::string msg = state.str();
        for (auto& pair : players) {
            send(pair.second->get_socket(), msg.c_str(), msg.length(), 0);
        }
    }

    void print_status() {
        static int counter = 0;
        if (++counter % 300 == 0) {
            std::cout << "\n[STATUS] Running... Players: " << players.size() << "\n";
            for (auto& pair : players) {
                Player* p = pair.second;
                std::cout << "  - Player " << p->get_id() << ": " << p->get_name()
                          << " at (" << p->get_x() << ", " << p->get_y() << ")\n";
            }
        }
    }

    void run() {
        std::cout << "\nServer running on port " << port << "\n";
        std::cout << "Using " << serializer->getName() << " serialization\n";
        std::cout << "Waiting for clients...\n";
        std::cout << "Press Ctrl+C to stop.\n\n";

        while (true) {
            accept_connections();
            receive_messages();
            broadcast_state();
            print_status();
            usleep(16666);  // ~60 FPS
        }
    }
};

int main(int argc, char* argv[]) {
    int port = 8080;
    std::string game_name = "UnknownGame";

    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        if ((arg == "--port" || arg == "-p") && i + 1 < argc) port = std::atoi(argv[++i]);
        else if ((arg == "--name" || arg == "-n") && i + 1 < argc) game_name = argv[++i];
    }

    GameServer server(port, game_name);
    server.run();
    return 0;
}