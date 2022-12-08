#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <err.h>
#include <errno.h>

#include <unistd.h>
#include <fcntl.h>
#include <libaio.h>

#define BLOCK_SIZE 4096

int main(int argc, char *argv[]) {
    char device[64];
    char mode = 'r';

	io_context_t ctx;
	struct iocb iocb;
	struct iocb * iocbs[1];
	struct io_event events[1];
	struct timespec timeout;
	int fd;
    
    struct timeval start_tv, end_tv;
    long start, end, time_spent;
    

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
	if (fd < 0) err(1, "open");

	memset(&ctx, 0, sizeof(ctx));
	if (io_setup(10, &ctx) != 0) err(1, "io_setup");

	void *buff;
    posix_memalign(&buff, BLOCK_SIZE, BLOCK_SIZE);
    srand(time(NULL));

    gettimeofday(&start_tv, NULL);


	io_prep_pread(&iocb, fd, buff, 4096, 123456*4096);
	iocb.data = buff;

	iocbs[0] = &iocb;


    

	if (io_submit(ctx, 1, iocbs) != 1) {
		io_destroy(ctx);
		err(1, "io_submit");
	}

	while (1) {
		timeout.tv_sec = 0;
		timeout.tv_nsec = 500000000;
		if (io_getevents(ctx, 0, 1, events, &timeout) == 1) {
            printf("%s!\n", (char*)buff);
			close(fd);
			break;
		}
		printf("not done yet\n");
	}

    gettimeofday(&end_tv, NULL);
    start = start_tv.tv_sec * 1000000 + start_tv.tv_usec;
    end = end_tv.tv_sec * 1000000 + end_tv.tv_usec;
    time_spent = (end - start);
    printf("%ld\n", time_spent);
	io_destroy(ctx);

	return 0;
}