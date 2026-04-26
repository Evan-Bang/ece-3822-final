# Makefile for Project 2 - Game Server with Position Buffering
#
# Directory structure:
#   include/  - Header files (.h)
#   src/      - Source files (.cpp)
#
# Usage:
#   make                                    # TEXT + PositionSmoother (defaults)
#   make SERIALIZER=TEXT BUFFER=SMOOTHER    # TEXT + PositionSmoother
#   make SERIALIZER=JSON BUFFER=SMOOTHER    # JSON + PositionSmoother
#   make SERIALIZER=BINARY BUFFER=JITTER    # BINARY + JitterBuffer
#   make test                               # Build and run buffer tests
#   make all                                # Build server + tests
#   make clean                              # Remove all compiled files
#   make help                               # Show all options

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -I include

# ============================================
# SERIALIZER SELECTION (default: TEXT)
# ============================================
SERIALIZER ?= TEXT

ifeq ($(SERIALIZER), JSON)
    CXXFLAGS += -DUSE_JSON
    SER_SUFFIX = _json
else ifeq ($(SERIALIZER), BINARY)
    CXXFLAGS += -DUSE_BINARY
    SER_SUFFIX = _binary
else
    SER_SUFFIX = _text
endif

# ============================================
# BUFFER STRATEGY SELECTION (default: SMOOTHER)
# ============================================
BUFFER ?= SMOOTHER

ifeq ($(BUFFER), JITTER)
    CXXFLAGS += -DUSE_JITTER_BUFFER
    BUF_SUFFIX = _jitter
else
    CXXFLAGS += -DUSE_POSITION_SMOOTHER
    BUF_SUFFIX = _smoother
endif

SUFFIX = $(SER_SUFFIX)$(BUF_SUFFIX)

SRC_DIR = src
INC_DIR = include
OBJ_DIR = obj$(SUFFIX)

$(shell mkdir -p $(OBJ_DIR))

# Server object files - ADDED bloom_filter.o HERE
SERVER_OBJS = $(OBJ_DIR)/player.o $(OBJ_DIR)/text_serializer.o \
              $(OBJ_DIR)/json_serializer.o $(OBJ_DIR)/binary_serializer.o \
              $(OBJ_DIR)/platform_sum.o $(OBJ_DIR)/bloom_filter.o

# Buffer object files
BUFFER_OBJS = $(OBJ_DIR)/position_smoother.o $(OBJ_DIR)/jitter_buffer.o

# Default target
server: server$(SUFFIX)

all: server$(SUFFIX) test_buffers

# Link server
server$(SUFFIX): $(SRC_DIR)/server.cpp $(SERVER_OBJS) $(BUFFER_OBJS)
	$(CXX) $(CXXFLAGS) -o server$(SUFFIX) $(SRC_DIR)/server.cpp $(SERVER_OBJS) $(BUFFER_OBJS)
	@echo "Server compiled successfully: server$(SUFFIX)"

test_buffers: $(SRC_DIR)/test_buffers.cpp $(BUFFER_OBJS)
	$(CXX) $(CXXFLAGS) -o test_buffers $(SRC_DIR)/test_buffers.cpp $(BUFFER_OBJS)

test: test_buffers
	./test_buffers

# --- Compilation Rules ---

$(OBJ_DIR)/player.o: $(SRC_DIR)/player.cpp $(INC_DIR)/player.h
	$(CXX) $(CXXFLAGS) -c $(SRC_DIR)/player.cpp -o $(OBJ_DIR)/player.o

$(OBJ_DIR)/text_serializer.o: $(SRC_DIR)/text_serializer.cpp $(INC_DIR)/text_serializer.h
	$(CXX) $(CXXFLAGS) -c $(SRC_DIR)/text_serializer.cpp -o $(OBJ_DIR)/text_serializer.o

$(OBJ_DIR)/json_serializer.o: $(SRC_DIR)/json_serializer.cpp $(INC_DIR)/json_serializer.h
	$(CXX) $(CXXFLAGS) -c $(SRC_DIR)/json_serializer.cpp -o $(OBJ_DIR)/json_serializer.o

$(OBJ_DIR)/binary_serializer.o: $(SRC_DIR)/binary_serializer.cpp $(INC_DIR)/binary_serializer.h
	$(CXX) $(CXXFLAGS) -c $(SRC_DIR)/binary_serializer.cpp -o $(OBJ_DIR)/binary_serializer.o

$(OBJ_DIR)/platform_sum.o: $(SRC_DIR)/platform_sum.cpp $(INC_DIR)/platform_sum.h
	$(CXX) $(CXXFLAGS) -c $(SRC_DIR)/platform_sum.cpp -o $(OBJ_DIR)/platform_sum.o

# NEW: Rule for Bloom Filter
$(OBJ_DIR)/bloom_filter.o: $(SRC_DIR)/bloom_filter.cpp $(INC_DIR)/bloom_filter.h
	$(CXX) $(CXXFLAGS) -c $(SRC_DIR)/bloom_filter.cpp -o $(OBJ_DIR)/bloom_filter.o

$(OBJ_DIR)/position_smoother.o: $(SRC_DIR)/position_smoother.cpp $(INC_DIR)/position_smoother.h
	$(CXX) $(CXXFLAGS) -c $(SRC_DIR)/position_smoother.cpp -o $(OBJ_DIR)/position_smoother.o

$(OBJ_DIR)/jitter_buffer.o: $(SRC_DIR)/jitter_buffer.cpp $(INC_DIR)/jitter_buffer.h
	$(CXX) $(CXXFLAGS) -c $(SRC_DIR)/jitter_buffer.cpp -o $(OBJ_DIR)/jitter_buffer.o

clean:
	rm -rf obj_* server_* test_buffers

help:
	@echo "Usage: make SERIALIZER=[TEXT|JSON|BINARY] BUFFER=[SMOOTHER|JITTER]"

.PHONY: all server test clean help