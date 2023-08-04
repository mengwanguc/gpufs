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

#include <pthread.h>


#define NUM_FILES 1281167
#define NUM_READS 1000


typedef struct sample {
    int index;
    int inode;
} Sample;

char filepaths[NUM_FILES][100];
Sample samples[NUM_READS];



int main(int argc, char *argv[]) {
    int i;
    FILE *fpaths;
    FILE *fsamples;
    FILE *fsamples_inodes;
    char fsamples_name[100], fsamples_inodes_name[100];

    struct timeval start_tv, end_tv;
    long start, end, time_spent;

    int mode = 0;

    if(argc <= 1) {
        printf("Please specify paths file\n./read [/imagenette_file_paths]\n");
        exit(1);
    }

    // file paths
    fpaths = fopen(argv[1], "r");
    i = 0;
    while(fscanf(fpaths, "%s", filepaths[i]) == 1){
            i++;
    }
    fclose(fpaths);
    // printf("%d\n", i);
    // printf("%s\n", filepaths[NUM_FILES-1]);

    // sampling
    snprintf(fsamples_name, 100, "samples_%d.txt", NUM_READS);
    fsamples = fopen(fsamples_name, "r");
    snprintf(fsamples_inodes_name, 100, "samples_inodes_%d.txt", NUM_READS);
    fsamples_inodes = fopen(fsamples_inodes_name, "w");
    
    i = 0;
    while(fscanf(fsamples, "%d", &samples[i].index) == 1){
            i++;
    }
    fclose(fsamples);

    for (i = 0; i < NUM_READS; i++) {
        int fd = open(filepaths[samples[i].index], O_RDONLY);
        if(fd == -1) {
            perror("Error: File open failure.");
        }
        else {
            struct stat file_stat;  
            int ret;  
            ret = fstat (fd, &file_stat);  
            if (ret < 0) {  
                perror("Error: fstat failure.");
            }
            samples[i].inode = file_stat.st_ino;
        }
        close(fd);
    }

    for (i = 0; i < NUM_READS; i++) {
        fprintf(fsamples_inodes, "%d %u\n", samples[i].index, samples[i].inode);
    }


    fclose(fsamples_inodes);

    return 0;
}    