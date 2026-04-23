#ifndef SUM_H
#define SUM_H

#include <string>

// Function to send the final game stats to the Python Arcade Server
void report_to_python(const std::string& name, int score, long playtime);
int get_port_from_config(const std::string& key);
#endif