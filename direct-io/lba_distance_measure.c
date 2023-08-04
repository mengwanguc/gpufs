#define _GNU_SOURCE
 
#include <sys/time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>
#include <fcntl.h>
#include <time.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>
 
#define BLOCK_SIZE 4096
#define BLOCK_COUNT 104857600 // 100 million blocks. 400GB data
#define NUM_SAMPLES 10

int cmpfunc (const void * a, const void * b) {
   return ( *(int*)a - *(int*)b );
}
 
int main(int argc, char *argv[]) {
        char device[64];
        void *buff;
        int i;
        int fd;
        long rand_byte;
        int mem;
        long seek;
        int read_result;
        struct timeval start_tv, end_tv;
        long start, end, time_spent;
        long latencies[NUM_SAMPLES];
        long all_byte = (long) BLOCK_SIZE * BLOCK_COUNT;
        char mode = 'r';
        FILE *fp;
        long block_index[1000];
        long distance_kb, distance_byte;
        long start_byte;

        int buffer_size = BLOCK_SIZE;

        if(argc <= 1) {
                printf("Please specify device name and mode\n./direct_io [/dev/sda]\n");
                exit(1);
        } else {
                sprintf(device, "%s", argv[1]);
        }
        fd = open(device, O_DIRECT | O_SYNC | O_RDWR);
        if(fd < 0) {
                printf("Cannot open %s. Error: %d\n", device, fd);
                exit(1);
        }

        srand(time(NULL));
        posix_memalign(&buff, BLOCK_SIZE, buffer_size);
        for (distance_kb = 0; distance_kb < 1024*1024; distance_kb += 32) {
                
                for(i = 0; i < NUM_SAMPLES; ++i) {
                        rand_byte = (rand() / (double) RAND_MAX) * BLOCK_COUNT;
                        rand_byte *= BLOCK_SIZE;
                        seek = lseek(fd, rand_byte, SEEK_SET);
                        if(seek < 0) {
                                printf("Cannot seek %ld\n", rand_byte);
                                continue;
                        }
                        read_result = read(fd, buff, buffer_size);
                        start_byte = rand_byte + BLOCK_SIZE + distance_kb * 1024;
                        seek = lseek(fd, start_byte, SEEK_SET);
                        gettimeofday(&start_tv, NULL);
                        read_result = read(fd, buff, buffer_size);
                        gettimeofday(&end_tv, NULL);
                        start = start_tv.tv_sec * 1000000 + start_tv.tv_usec;
                        end = end_tv.tv_sec * 1000000 + end_tv.tv_usec;
                        time_spent = (end - start);
                        latencies[i] = time_spent;
                }
                printf("%ldKB:\t", distance_kb);
                for(i = 0; i < NUM_SAMPLES; ++i) {
                        printf("%ld\t", latencies[i]);
                }
                printf("\n");
        }
        close(fd);
        return 0;
}