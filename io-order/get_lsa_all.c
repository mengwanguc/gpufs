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
// #define NUM_FILES 9469
#define NUM_READS 10000


typedef struct sample {
    int index;
    int inode;
    __u64 start_physical;
} Sample;

char filepaths[NUM_FILES][100];
Sample samples[NUM_FILES];


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
    FILE *fall_inodes_lba;

    struct timeval start_tv, end_tv;
    long start, end, time_spent;

    int mode = 0;

    if(argc <= 1) {
        printf("Please specify paths file\n./get_lsa_all [/imagenette_file_paths]\n");
        exit(1);
    }

    // file paths
    fpaths = fopen(argv[1], "r");
    if(!fpaths) {
        perror("Error: fpaths open failure.");
        exit(1);
    }
    for (i = 0; i < NUM_FILES; i++){
        fscanf(fpaths, "%s", filepaths[i]);
    }
        

    fclose(fpaths);
    printf("%d\n", i);
    // printf("%s\n", filepaths[NUM_FILES-1]);

    for (i = 0; i < NUM_FILES; i++) {
        samples[i].index = i;
        int fd = open(filepaths[i], O_RDONLY);
        if(fd == -1) {
            perror("Error: File open failure.");
        }
        else {
            // get inode
            struct stat file_stat;  
            int ret;  
            ret = fstat (fd, &file_stat);  
            if (ret < 0) {  
                perror("Error: fstat failure.");
            }
            samples[i].inode = file_stat.st_ino;

            // get lba
            struct fiemap *fiemap;

			if ((fiemap = read_fiemap(fd)) != NULL) 
				samples[i].start_physical = fiemap->fm_extents[0].fe_physical;
			close(fd);
        }
        close(fd);
    }


    fall_inodes_lba = fopen("all_inodes_lba", "w");

    for (i = 0; i < NUM_FILES; i++) {
        fprintf(fall_inodes_lba, "%d %u %llu\n", 
                samples[i].index, samples[i].inode, samples[i].start_physical);
    }


    fclose(fall_inodes_lba);

    return 0;
}    