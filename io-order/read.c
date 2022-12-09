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

long open_time = 0;
long read_time = 0;

typedef struct sample {
    int index;
    int inode;
} Sample;

pthread_mutex_t count_mutex;
int count;

char filepaths[NUM_FILES][100];
Sample samples[NUM_READS];


int cmp_by_index_func (const void * a, const void * b) {
   return ( ((Sample*)a)->index - ((Sample*)b)->index );
}

int cmp_by_inode_func (const void * a, const void * b) {
   return ( ((Sample*)a)->inode - ((Sample*)b)->inode );
}

void *sort_by_inode() {
    int i;
    for (i = 0; i < NUM_READS; i++) {
        int fd = open(filepaths[samples[i].index], O_RDONLY | O_DIRECT);
        if(fd == -1) {
            perror("Error: File open failure.");
        }
        else {
            // struct stat file_stat;  
            // int ret;  
            // ret = fstat (fd, &file_stat);  
            // if (ret < 0) {  
            //     perror("Error: fstat failure.");
            // }
            // samples[i].inode = file_stat.st_ino;
            printf("%u\n", samples[i].inode );
        }
        close(fd);
    }
    qsort(samples, NUM_READS, sizeof(Sample), cmp_by_inode_func);
    return;
}

void *thread_read(void *param)
{
    int cur = 0;
    char *string = malloc(50000000);
    struct timeval start_tv, end_tv;
    long start, end, time_spent;


    while (cur < NUM_READS) {
        pthread_mutex_lock(&count_mutex);
        cur = count++;
        pthread_mutex_unlock(&count_mutex);
        if (cur >= NUM_READS) {
            break;
        }

        gettimeofday(&start_tv, NULL);
        int f = open(filepaths[samples[cur].index], O_RDONLY);
        gettimeofday(&end_tv, NULL);
        start = start_tv.tv_sec * 1000000 + start_tv.tv_usec;
        end = end_tv.tv_sec * 1000000 + end_tv.tv_usec;
        time_spent = (end - start);
        open_time += time_spent;
        // printf("open time: %ld\n", time_spent);

        if(f == -1) {
            perror("Error: File open failure.");
        }
        else {
            gettimeofday(&start_tv, NULL);

            long fsize = lseek(f, 0, SEEK_END);
            lseek(f, 0, SEEK_SET);  /* same as rewind(f); */
            int ret = read(f, string, fsize);

            gettimeofday(&end_tv, NULL);
            start = start_tv.tv_sec * 1000000 + start_tv.tv_usec;
            end = end_tv.tv_sec * 1000000 + end_tv.tv_usec;
            time_spent = (end - start);
            read_time += time_spent;
            // printf("read time: %ld\n", time_spent);

            close(f);
            // printf("%d\n", ret);
            string[fsize] = 0;
        }

    }
    // printf("%d\n", cur);
    return NULL;
}


int main(int argc, char *argv[]) {
    int i;
    FILE *fpaths;
    FILE *fsamples;

    struct timeval start_tv, end_tv;
    long start, end, time_spent;

    int mode = 0;

    if(argc <= 3) {
        printf("Please specify paths file\n./read [/imagenette_file_paths] [num_threads] [mode: 0 for unsort, 1 for partial sort, 2 for all sort,"
                        "3 for sort by inode number]\n");
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
    fsamples = fopen("samples_1000.txt", "r");
    i = 0;
    while(fscanf(fsamples, "%d", &samples[i].index) == 1){
            i++;
    }
    fclose(fsamples);
    // printf("%d\n", i);
    // printf("%d\n", samples[NUM_READS-1]);
    
    mode = atoi(argv[3]);

    gettimeofday(&start_tv, NULL);

    if (mode == 1) {
        int batch = 100;
        for(i = 0; i < NUM_READS; i += batch) {
            qsort(&samples[i], batch, sizeof(Sample), cmp_by_index_func);
        }
    } else if (mode == 2) {
        qsort(samples, NUM_READS, sizeof(Sample), cmp_by_index_func);
    } else if (mode == 3) {
        sort_by_inode();
    }

    gettimeofday(&end_tv, NULL);
    start = start_tv.tv_sec * 1000000 + start_tv.tv_usec;
    end = end_tv.tv_sec * 1000000 + end_tv.tv_usec;
    time_spent = (end - start);
    printf("sort time: %ld\n", time_spent);


    int num_threads = atoi(argv[2]);
    pthread_t *tid_array = malloc(num_threads * sizeof(pthread_t));

    // create all threads
    gettimeofday(&start_tv, NULL);

    for(i = 0; i < num_threads; i++)
    {
       pthread_create(&tid_array[i], NULL, thread_read, NULL);
    }

    for(i = 0; i < num_threads; i++)
    {
        pthread_join(tid_array[i], NULL);
    }

    gettimeofday(&end_tv, NULL);
    start = start_tv.tv_sec * 1000000 + start_tv.tv_usec;
    end = end_tv.tv_sec * 1000000 + end_tv.tv_usec;
    time_spent = (end - start);

    printf("%ld\n", time_spent);

    printf("open time:%ld\n", open_time);
    printf("read time:%ld\n", read_time);

    free(tid_array);

    return 0;
}    