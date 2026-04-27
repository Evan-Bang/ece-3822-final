#include "bloom_filter.h"

// FNV 1-a hashing algorithm. 
size_t BloomFilter::get_hash(std::string const& s, int iteration) {
    unsigned long long hash = 14695981039346656037ULL; // FNV offset basis
    const unsigned long long fnv_prime = 1099511628211ULL; //Prime

    // Standard FNV-1a logic
    for (char const &c : s) {
        hash ^= static_cast<unsigned char>(c);
        hash *= fnv_prime;
    }

    // We do this so we can get multiple different hashes out of one function
    hash ^= iteration;
    hash *= fnv_prime;

    return static_cast<size_t>(hash % size);
}

void BloomFilter::add_word(std::string const& s) {
    for (int i = 0; i < num_hashes; ++i) {
        size_t index = get_hash(s, i);
        bit_array[index] = true;
    }
}

bool BloomFilter::check_word(std::string const& s) {
    for (int i = 0; i < num_hashes; ++i) {
        size_t index = get_hash(s, i);
        if (!bit_array[index]) {
            return false;
        }
    }
    return true;
}