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
#define BLOCK_COUNT 10485760

int cmpfunc (const void * a, const void * b) {
   return ( *(int*)a - *(int*)b );
}
 
int main(int argc, char *argv[]) {
        char device[64];
        int random;
        void *buff;
        int i;
        int fd;
        long rand_byte;
        int mem;
        long seek;
        int read_result;
        struct timeval start_tv, end_tv;
        long start, end, time_spent;
        long all_byte = (long) BLOCK_SIZE * BLOCK_COUNT;
        char mode = 'r';
        FILE *fp;
        long block_index[1000];

        int buffer_size = BLOCK_SIZE * 1000;

        if(argc <= 2) {
                printf("Please specify device name and mode\n./direct_io [/dev/sda] [s/r]\n");
                exit(1);
        } else {
                sprintf(device, "%s", argv[1]);
                mode = argv[2][0];
                if (!(mode == 'r' || mode == 's')) {
                        printf("mode should be 's' for sequential or 'r' for random\n");
                        exit(1);
                }
        }
        fd = open(device, O_DIRECT | O_SYNC | O_RDWR);
        if(fd < 0) {
                printf("Cannot open %s. Error: %d\n", device, fd);
                exit(1);
        }
        fp = fopen("random.txt", "r");

        i = 0;
        while(fscanf(fp, "%ld", &block_index[i]) == 1){
                i++;
        }
        fclose(fp);
        if (mode == 's') {
                qsort(block_index, 1000, sizeof(long), cmpfunc);
        }

        srand(time(NULL));
        posix_memalign(&buff, BLOCK_SIZE, buffer_size);
        int step = BLOCK_COUNT / 1000;
        long total = 0;
        for(i = 0; i < 1000; ++i) {
                rand_byte = block_index[i];
                rand_byte *= BLOCK_SIZE;
                seek = lseek(fd, rand_byte, SEEK_SET);
                if(seek < 0) {
                        printf("Cannot seek %ld\n", rand_byte);
                        continue;
                }
                gettimeofday(&start_tv, NULL);
                read_result = read(fd, buff, buffer_size);
                gettimeofday(&end_tv, NULL);
                start = start_tv.tv_sec * 1000000 + start_tv.tv_usec;
                end = end_tv.tv_sec * 1000000 + end_tv.tv_usec;
                time_spent = (end - start);
                total += time_spent;
                printf("%ld\n", time_spent);
        }
        printf("avg:%ld\n", total/1000);
        close(fd);
        return 0;
}