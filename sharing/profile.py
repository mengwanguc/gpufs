import subprocess
from time import clock_gettime, CLOCK_MONOTONIC

GPU_BND_CMD_FMT = (
    "python main-emulator-share.py  "
    "--epoch {n_epoch} --profile-batches -1 --workers 8 --gpu-type=p100 "
    "--gpu-count=1 --arch=resnet50 --emulator-version=1 ~/data/test-accuracy/"
)

CPU_BND_CMD_FMT = (
    "python main-emulator-share.py  "
    "--epoch {n_epoch} --profile-batches -1 --workers 8 --gpu-type=p100 "
    "--gpu-count=1 --arch=alexnet --emulator-version=1 ~/data/test-accuracy/"
)



def main():
    # for n_epoch in range(1, 6):
    #     cmd: list[str] = GPU_BND_CMD_FMT.format(n_epoch=n_epoch).split()
    #     st = clock_gettime(CLOCK_MONOTONIC)
    #     subprocess.run(cmd, capture_output=True)
    #     end = clock_gettime(CLOCK_MONOTONIC)
    #     print(f"{n_epoch},{end-st}")
    
    print("-----------------------------------------------------------------")
    for n_epoch in range(16, 20):
        cmd: list[str] = CPU_BND_CMD_FMT.format(n_epoch=n_epoch).split()
        st = clock_gettime(CLOCK_MONOTONIC)
        subprocess.run(cmd, capture_output=True)
        end = clock_gettime(CLOCK_MONOTONIC)
        print(f"{n_epoch},{end-st}")


if __name__ == "__main__":
    main()
