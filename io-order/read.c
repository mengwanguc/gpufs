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
#define NUM_READS 10000

pthread_mutex_t count_mutex;
int count;

char filepaths[NUM_FILES][100];
int samples[NUM_READS];


int cmpfunc (const void * a, const void * b) {
   return ( *(int*)a - *(int*)b );
}

void *thread_read(void *param)
{
    int cur = 0;
    char *string = malloc(50000000);
    while (cur < NUM_READS) {
        pthread_mutex_lock(&count_mutex);
        cur = count++;
        pthread_mutex_unlock(&count_mutex);
        if (cur >= NUM_READS) {
            break;
        }

        int f = open(filepaths[samples[cur]], O_RDONLY);
        if(f == -1) {
            perror("Error: File open failure.");
        }
        else {
            long fsize = lseek(f, 0, SEEK_END);
            lseek(f, 0, SEEK_SET);  /* same as rewind(f); */
            int ret = read(f, string, fsize);
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
        printf("Please specify paths file\n./read [/imagenette_file_paths] [num_threads] [mode: 0 for unsort, 1 for partial sort, 2 for all sort]\n");
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
    fsamples = fopen("samples_10000.txt", "r");
    i = 0;
    while(fscanf(fsamples, "%d", &samples[i]) == 1){
            i++;
    }
    fclose(fsamples);
    // printf("%d\n", i);
    // printf("%d\n", samples[NUM_READS-1]);

    
    mode = atoi(argv[3]);
    if (mode == 1) {
        int batch = 100;
        for(i = 0; i < NUM_READS; i += batch) {
            qsort(&samples[i], batch, sizeof(int), cmpfunc);
        }
    } else if (mode == 2) {
        qsort(samples, NUM_READS, sizeof(int), cmpfunc);
    }

    // for(i = 0; i < NUM_READS; i++) {
    //     printf("%d\n", samples[i]);
    // }


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

    free(tid_array);

    return 0;
}    