/*
position_smoother.cpp - Implementation of PositionSmoother class

Author: Owen Ringrose
Date: 2/24/2026
Project: Project 2 - Network Position Buffering
*/

#include "position_smoother.h"
#include "position.h"
#include <stdexcept>
#include <cmath>

void PositionSmoother::add_position(float x, float y, long timestamp) {
    // Add a new position to the buffer, dropping oldest if full
    Position p(x, y, timestamp);
    if (!enqueue(p)) {
        dequeue();
        enqueue(p);
    }
}

Position PositionSmoother::get_simple_average() const {
    // Simple average of all positions in buffer
    if (is_empty()){
        throw std::runtime_error("Buffer is empty");
    }
    float sum_x = 0;
    float sum_y = 0;
    int buffer_size = size();
    for (int i = 0; i < buffer_size; i++){
        Position pos = get(i);
        sum_x += pos.x;
        sum_y += pos.y;
    }
    float avg_x = sum_x/buffer_size;
    float avg_y = sum_y/buffer_size;

    return Position(avg_x, avg_y);
}

Position PositionSmoother::get_weighted_average() const {
    // Weighted average - recent positions weighted more heavily
    if (is_empty()){
        throw std::runtime_error("Buffer is empty");
    }
    int buffer_size = size();
    float sum_x = 0;
    float sum_y = 0; 
    int total_weight = 0;
    int weight = 0;
    for (int i = 0; i < buffer_size; i++){
        // Weights are equal to the index in the list + 1.
        weight = i + 1;
        Position p = get(i);
        sum_x += p.x * weight;
        sum_y += p.y * weight;
        total_weight += weight; 
    }
    float avg_x = sum_x / total_weight;
    float avg_y = sum_y / total_weight;

    return Position(avg_x, avg_y);
}

Position PositionSmoother::get_exponential_smooth(float alpha) const {
    // BONUS: Implement exponential smoothing
    // TODO: Check if buffer is empty
    // TODO: Start with first position as initial smooth value
    // TODO: For each subsequent position:
    //       - smooth_x = alpha * pos.x + (1-alpha) * smooth_x
    //       - smooth_y = alpha * pos.y + (1-alpha) * smooth_y
    // TODO: Return final smoothed position
   if (is_empty()) {
        throw std::runtime_error("Buffer is empty");
    }
    float smooth_x = get(0).x;
    float smooth_y = get(0).y;

    for (int i = 1; i < size(); i++) {  // start at 1, skip first
        Position p = get(i);
        smooth_x = alpha * p.x + (1 - alpha) * smooth_x;
        smooth_y = alpha * p.y + (1 - alpha) * smooth_y;
    }
    return Position(smooth_x, smooth_y);
}

Position PositionSmoother::get_latest() const {
    // Get the most recent position
    if (is_empty()){
        throw std::runtime_error("Buffer is empty");
    }
    return get(size() - 1);
}

float PositionSmoother::get_variance() const {
    if (is_empty()) {
        return 0.0f;
    }
    
    // Calculate mean
    Position mean = get_simple_average();
    
    // Calculate variance: average of squared distances from mean
    float sum_sq_dist = 0.0f;
    for (int i = 0; i < size(); i++) {
        Position p = get(i);
        float dx = p.x - mean.x;
        float dy = p.y - mean.y;
        sum_sq_dist += (dx*dx + dy*dy);
    }
    
    return std::sqrt(sum_sq_dist / size());
}
