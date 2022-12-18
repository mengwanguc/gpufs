#define _GNU_SOURCE
#include <sys/time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>

#include <stdio.h>
#include <fcntl.h>
#include <time.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

#include <pthread.h>

#include <linux/fs.h>
#include <linux/fiemap.h>


#define NUM_FILES 1281167
#define NUM_READS 100000


typedef struct sample {
    int index;
    int inode;
    __u64 start_physical;
} Sample;

char filepaths[NUM_FILES][100];
Sample samples[NUM_READS];


struct fiemap *read_fiemap(int fd)
{
	struct fiemap *fiemap;
	int extents_size;

	if ((fiemap = (struct fiemap*)malloc(sizeof(struct fiemap))) == NULL) {
		fprintf(stderr, "Out of memory allocating fiemap\n");	
		return NULL;
	}
	memset(fiemap, 0, sizeof(struct fiemap));

	fiemap->fm_start = 0;
	fiemap->fm_length = ~0;		/* Lazy */
	fiemap->fm_flags = 0;
	fiemap->fm_extent_count = 0;
	fiemap->fm_mapped_extents = 0;

	/* Find out how many extents there are */
	if (ioctl(fd, FS_IOC_FIEMAP, fiemap) < 0) {
		fprintf(stderr, "fiemap ioctl() failed\n");
		return NULL;
	}

	/* Read in the extents */
	extents_size = sizeof(struct fiemap_extent) * 
                              (fiemap->fm_mapped_extents);

	/* Resize fiemap to allow us to read in the extents */
	if ((fiemap = (struct fiemap*)realloc(fiemap,sizeof(struct fiemap) + 
                                         extents_size)) == NULL) {
		fprintf(stderr, "Out of memory allocating fiemap\n");	
		return NULL;
	}

	memset(fiemap->fm_extents, 0, extents_size);
	fiemap->fm_extent_count = fiemap->fm_mapped_extents;
	fiemap->fm_mapped_extents = 0;

	if (ioctl(fd, FS_IOC_FIEMAP, fiemap) < 0) {
		fprintf(stderr, "fiemap ioctl() failed\n");
		return NULL;
	}
	
	return fiemap;
}

void dump_fiemap(struct fiemap *fiemap, char *filename)
{
	int i;

	printf("File %s has %d extents:\n",filename, fiemap->fm_mapped_extents);

	printf("#\tLogical          Physical         Length           Flags\n");
	for (i=0;i<fiemap->fm_mapped_extents;i++) {
		printf("%d:\t%-16.llu %-16.llu %-16.llu %-4.u\n",
			i,
			fiemap->fm_extents[i].fe_logical,
			fiemap->fm_extents[i].fe_physical,
			fiemap->fm_extents[i].fe_length,
			fiemap->fm_extents[i].fe_flags);
        printf("%d:\t%-16.llu %-16.llu %-16.llu %-4.u\n",
			i,
			fiemap->fm_extents[i].fe_logical/512,
			fiemap->fm_extents[i].fe_physical/512,
			fiemap->fm_extents[i].fe_length/512,
			fiemap->fm_extents[i].fe_flags);
	}
	printf("\n");
}


int main(int argc, char *argv[]) {
    int i;
    FILE *fpaths;
    FILE *fsamples;
    FILE *fsamples_inodes_lba;
    char fsamples_name[100], fsamples_inodes_lba_name[100];

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
    snprintf(fsamples_inodes_lba_name, 100, "samples_inodes_lba_%d.txt", NUM_READS);
    fsamples_inodes_lba = fopen(fsamples_inodes_lba_name, "w");
    
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
        printf("%d %s\n", i, filepaths[samples[i].index]);
        int fd = open(filepaths[samples[i].index], O_RDONLY);
        if(fd == -1) {
            perror("Error: File open failure.");
        }
        else {
            struct fiemap *fiemap;

			if ((fiemap = read_fiemap(fd)) != NULL) 
				samples[i].start_physical = fiemap->fm_extents[0].fe_physical;
			close(fd);
        }
    }

    for (i = 0; i < NUM_READS; i++) {
        fprintf(fsamples_inodes_lba, "%d %u %llu\n", 
                samples[i].index, samples[i].inode, samples[i].start_physical);
    }


    fclose(fsamples_inodes_lba);

    return 0;
}    