#include "heap_driver.h"
#include <stdint.h>
#include <stddef.h>
#include <string.h>

#define HEAP_START_ADDR  ((uint8_t*)0x20001000)
#define HEAP_SIZE        (4 * 1024)
#define BLOCK_SIZE       16
#define BLOCK_COUNT      (HEAP_SIZE / BLOCK_SIZE)

// Students should be provided the above code (includes and defines) and the function declarations in this file.
// They can figure out the rest.

// Allocation bitmap: 0 = free, 1 = used

// Add you code below

uint8_t storage[BLOCK_COUNT];

void heap_init() {
    for (int i = 0 ; i < BLOCK_COUNT ; i++) storage[i] = 0;
}

void* heap_alloc(size_t size) {
    if (size == 0) return NULL;
    int n = (size + BLOCK_SIZE - 1) / BLOCK_SIZE;
    int flag = 0;
    for (int i = 0 ; i < BLOCK_COUNT ; i++) {
        if (i + n > BLOCK_COUNT) return NULL;
        if (storage[i] == 0) {
            flag = 1;
            for (int j = 0 ; j < n ; j++) {
                if (i + j < BLOCK_COUNT && storage[i + j] == 1) {
                    flag = 0;
                    break;
                }
            }
            if (flag == 1) {
                for (int j = 0 ; j < n ; j++) storage[i + j] = 1;
                return (void*) (HEAP_START_ADDR + (i * BLOCK_SIZE));
            }
        }
    }
    return NULL;
}

void heap_free(void* ptr) {
    if (ptr == NULL) return;
    int n = ((uint8_t*)ptr - HEAP_START_ADDR) / BLOCK_SIZE;
    if (n < 0 || n >= BLOCK_COUNT) return;
    while (n < BLOCK_COUNT && storage[n] == 1) {
        storage[n] = 0;
        n++;
    }
}