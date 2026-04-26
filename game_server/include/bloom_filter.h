/*
bloom_filter.h
Bloom filter implementation for chat filtering.
Author: Owen Ringrose
Date: 4/25/2026
*/

#ifndef BLOOM_FILTER_H
#define BLOOM_FILTER_H

#include <string>
#include <vector>

class BloomFilter {
private:
    std::vector<bool> bit_array;
    int num_hashes;
    int size;

    size_t get_hash(std::string const& s, int iteration);

public:
    // Constructor
    BloomFilter(int m, int k) : num_hashes(k), size(m) {
        bit_array.resize(size, false);
    }

    void add_word(std::string const& s);

    bool check_word(std::string const& s);
    
    int get_word_count() const;
};

#endif
// End of file