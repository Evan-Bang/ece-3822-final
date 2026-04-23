#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>

#include "player.h"
#include "serializer.h"
#include "text_serializer.h"
#include "json_serializer.h"
#include "binary_serializer.h"

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
    std::map<int, std::string> recv_buffers;

    Serializer* serializer;
    int next_player_id = 1;
    int port;

public:
    GameServer(int port) : port(port) {
        serializer = new SERIALIZER_TYPE();

        server_socket = socket(AF_INET, SOCK_STREAM, 0);
        if (server_socket < 0) exit(1);

        int opt = 1;
        setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

        sockaddr_in address{};
        address.sin_family = AF_INET;
        address.sin_addr.s_addr = INADDR_ANY;
        address.sin_port = htons(port);

        if (bind(server_socket, (sockaddr*)&address, sizeof(address)) < 0) exit(1);
        if (listen(server_socket, 10) < 0) exit(1);

        fcntl(server_socket, F_SETFL, O_NONBLOCK);

        std::cout << "Server running on port " << port << "\n";
        std::cout << "Serializer: " << serializer->getName() << "\n";
    }

    ~GameServer() {
        for (auto& p : players) delete p.second;
        delete serializer;
        close(server_socket);
    }

    void accept_connections() {
        sockaddr_in client_addr{};
        socklen_t len = sizeof(client_addr);

        int client_socket = accept(server_socket, (sockaddr*)&client_addr, &len);
        if (client_socket < 0) return;

        fcntl(client_socket, F_SETFL, O_NONBLOCK);

        int id = next_player_id++;
        std::string name = "Player" + std::to_string(id);

        players[id] = new Player(id, name, 400, 300, client_socket);
        recv_buffers[id] = "";

        std::string welcome = "CONNECTED|" + std::to_string(id) + "\n";
        send(client_socket, welcome.c_str(), welcome.size(), 0);

        std::ifstream file("chat_history.txt");
        std::string line;

        while (std::getline(file, line)) {
            if (line.empty()) continue;

            std::istringstream ss(line);
            std::string n, t;

            std::getline(ss, n, '|');
            std::getline(ss, t);

            if (n.empty() || t.empty()) continue;

            std::string msg = "CHAT|" + n + "|" + t + "\n";
            send(client_socket, msg.c_str(), msg.size(), 0);
        }

        std::cout << "Player " << id << " connected\n";
    }

    void handle_chat(int sender_id, const std::string& line) {
        std::istringstream ss(line);

        std::string type;
        std::getline(ss, type, '|');
        if (type != "CHAT") return;

        std::string name, text;
        std::getline(ss, name, '|');
        std::getline(ss, text);

        if (name.empty() || text.empty()) return;

        std::string msg = "CHAT|" + name + "|" + text + "\n";

        for (auto& [id, p] : players) {
            if (id == sender_id) continue;
            send(p->get_socket(), msg.c_str(), msg.size(), 0);
        }

        std::ofstream file("chat_history.txt", std::ios::app);
        file << name << "|" << text << "\n";
    }

    void receive_messages() {
        char buffer[4096];
        std::vector<int> dead;

        for (auto& [id, player] : players) {
            int sock = player->get_socket();
            int n = recv(sock, buffer, sizeof(buffer) - 1, 0);

            if (n <= 0) {
                if (n == 0 || (errno != EAGAIN && errno != EWOULDBLOCK))
                    dead.push_back(id);
                continue;
            }

            buffer[n] = '\0';
            recv_buffers[id] += buffer;

            std::string& data = recv_buffers[id];
            size_t pos;

            while ((pos = data.find('\n')) != std::string::npos) {
                std::string line = data.substr(0, pos);
                data.erase(0, pos + 1);

                if (line.empty()) continue;

                std::istringstream ss(line);
                std::string type;
                std::getline(ss, type, '|');

                if (type == "CHAT") {
                    handle_chat(id, line);
                }
                else if (type == "UPDATE") {
                    std::string id_s, x_s, y_s, name, ctype, status;

                    std::getline(ss, id_s, '|');
                    std::getline(ss, x_s, '|');
                    std::getline(ss, y_s, '|');
                    std::getline(ss, name, '|');
                    std::getline(ss, ctype, '|');
                    std::getline(ss, status);

                    float x = std::stof(x_s);
                    float y = std::stof(y_s);

                    player->add_raw_position(x, y);
                    Position smoothed = player->get_smoothed_position();

                    player->set_position(smoothed.x, smoothed.y);
                    if (!name.empty()) player->set_name(name);
                    if (!ctype.empty()) player->set_character_type(ctype);
                    if (!status.empty()) player->set_status(status);
                }
            }
        }

        for (int id : dead) {
            close(players[id]->get_socket());
            delete players[id];
            players.erase(id);
            recv_buffers.erase(id);
        }
    }

    void broadcast_state() {
        if (players.empty()) return;

        std::ostringstream state;
        state << "STATE";

        for (auto& [id, p] : players)
            state << "||" << serializer->serialize(*p);

        state << "\n";

        std::string msg = state.str();

        for (auto& [id, p] : players)
            send(p->get_socket(), msg.c_str(), msg.size(), 0);
    }

    void run() {
        while (true) {
            accept_connections();
            receive_messages();
            broadcast_state();
            usleep(16666);
        }
    }
};

int main() {
    GameServer server(8080);
    server.run();
}