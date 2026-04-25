/*
jitter_buffer.cpp - Implementation of JitterBuffer class

Author: Owen Ringrose
Date: 2/24/2026
Project: Project 2 - Network Position Buffering
*/

#include "jitter_buffer.h"
#include <stdexcept>

// Constructor
//
JitterBuffer::JitterBuffer(int buffer_capacity, int min_size) 
    : CircularBuffer<Position>(buffer_capacity), 
      min_buffer_size(min_size), 
      playback_started(false), 
      start_timestamp(0) {
}

void JitterBuffer::add_position(float x, float y, long timestamp) {
   // Add a position to the buffer. Keeps the buffer at maximu capacity by dropping oldest if needed
    Position p(x, y, timestamp);

    if (!enqueue(p)){
        dequeue();
        enqueue(p);
    }

    if (!playback_started && size() >= min_buffer_size){
        playback_started = true;
        start_timestamp = timestamp;
    }
}

Position JitterBuffer::get_current_position() {
    // Return the position that should be displayed now, throwing an error if playback hasn't started yet or empty
    if (!playback_started){
        throw std::runtime_error("Buffering... waiting for minimum positions");
    }
    if(is_empty()){
        throw std::runtime_error("buffer underrun no positions avaliable");
    }
    return dequeue();
}

bool JitterBuffer::is_ready() const {
    // Return true if playback_started OR size() >= min_buffer_size
    return (playback_started || (size() >= min_buffer_size));
}

int JitterBuffer::get_latency_ms() const {
    // Gives an estimate of the latency added by buffering. 
    if (!playback_started){
        return 0;
    }
    // Assumed value change as needed.
    int average_time_between_updates = 50;
    int latency = size() * average_time_between_updates;
    return latency;
}

int JitterBuffer::get_buffer_health() const {
    // TODO: Return (size() * 100) / capacity
    return size() * 100 / capacity;
}

void JitterBuffer::reset() {
    // TODO: Call clear() to empty buffer
    // TODO: Set playback_started = false
    // TODO: Set start_timestamp = 0
    clear();
    playback_started = false;
    start_timestamp = 0;
}
