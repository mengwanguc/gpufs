import os
from pathlib import Path
from typing import Optional, Tuple, Union

from torch import Tensor
from torch import tensor
from torch.hub import download_url_to_file
from torch.utils.data import Dataset
from torchaudio.datasets.utils import _extract_tar, _load_waveform

import io
import soundfile as sf
from pydub import AudioSegment

FOLDER_IN_ARCHIVE = "SpeechCommands"
URL = "speech_commands_v0.02"
HASH_DIVIDER = "_nohash_"
EXCEPT_FOLDER = "_background_noise_"
SAMPLE_RATE = 16000
_CHECKSUMS = {
    "http://download.tensorflow.org/data/speech_commands_v0.01.tar.gz": "743935421bb51cccdb6bdd152e04c5c70274e935c82119ad7faeec31780d811d",  # noqa: E501
    "http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz": "af14739ee7dc311471de98f5f9d2c9191b18aedfe957f4a6ff791c709868ff58",  # noqa: E501
}


def _load_list(root, *filenames):
    output = []
    for filename in filenames:
        filepath = os.path.join(root, filename)
        with open(filepath) as fileobj:
            output += [os.path.normpath(os.path.join(root, line.strip())) for line in fileobj]
    return output


def _get_speechcommands_metadata(filepath: str, path: str) -> Tuple[str, int, str, str, int]:
    relpath = os.path.relpath(filepath, path)
    # print("relpath -> ", relpath)
    reldir, filename = os.path.split(relpath)
    # print("reldir, filename -> ", reldir, filename)
    _, label = os.path.split(reldir)
    # Besides the officially supported split method for datasets defined by "validation_list.txt"
    # and "testing_list.txt" over "speech_commands_v0.0x.tar.gz" archives, an alternative split
    # method referred to in paragraph 2-3 of Section 7.1, references 13 and 14 of the original
    # paper, and the checksums file from the tensorflow_datasets package [1] is also supported.
    # Some filenames in those "speech_commands_test_set_v0.0x.tar.gz" archives have the form
    # "xxx.wav.wav", so file extensions twice needs to be stripped twice.
    # [1] https://github.com/tensorflow/datasets/blob/master/tensorflow_datasets/url_checksums/speech_commands.txt
    speaker, _ = os.path.splitext(filename)
    speaker, _ = os.path.splitext(speaker)
    # print("speaker ->", speaker)

    speaker_id, utterance_number = speaker.split(HASH_DIVIDER)
    # print("speaker_id, utterance_number ->", speaker_id, utterance_number)
    utterance_number = int(utterance_number)

    return relpath, SAMPLE_RATE, label, speaker_id, utterance_number

def get_metadata_mytar(
    directory: str,
    group_size: int
):
    # print("directory ->", directory)
    directory = os.path.expanduser(directory)
    # print("directory2 ->", directory)
    metadata_path = os.path.join(directory, "metadata.txt")
    metadata = []
    classes = []
    subgroup = 0
    with open(metadata_path, 'r') as reader:
        # first get all classes
        class_count = int(reader.readline().strip())
        for _ in range(class_count):
            class_name = reader.readline().strip()
            classes.append(class_name)
        classes.sort()
        class_to_idx = {cls_name: i for i, cls_name in enumerate(classes)}
        print(class_to_idx)
        # then get all groups metadata
        while reader:
            groupname = reader.readline().strip().split(',')[0]
            if(groupname == ''):
                break
            group = []
            for i in range(group_size):
                values = reader.readline().strip().split(',')
                idx = values[0]
                audio_class = values[1]
                start = int(values[2])
                audio_size = int(values[3])
                audio_path = values[4]
                audio_class_idx = class_to_idx[audio_class]
                # group.append({'idx':idx, 'audio_class':audio_class, 'audio_class_idx':audio_class_idx, 'start':start, 'audio_size':audio_size, 'audio_path':audio_path})
                group = {'idx':idx, 'audio_class':audio_class, 'audio_class_idx':audio_class_idx, 'start':start, 'audio_size':audio_size, 'audio_path':audio_path}
                metadata.append({'groupname':groupname, 'subgroup':subgroup, 'metadata':group})
                subgroup += 1            
            # metadata.append({'groupname':groupname, 'metadata':group})
    print(class_to_idx)
    return metadata

def mytar_loader(path: str, group_metadata):
    waveforms = []
    labels = []
    speaker_ids = [] 
    utterance_numbers = []
    sample_rates = []
    # print("path ->", path)
    # # path = "/home/cc/gpufs/audio/grouped-data-audio/4/filegroup-0.mytar"
    # print("path2 ->", path)
    audio_info = group_metadata
    with open(path, 'rb') as f:
        f = f.read()
        # for audio_info in group_metadata:
        #     print("audio_info -> ", audio_info)
        audio_start = audio_info['start']
        audio_end = audio_start + audio_info['audio_size']
        audio_class = audio_info['audio_class']
        audio_path = audio_info['audio_path']
        # print('audio_class_idx:{}'.format(audio_class_idx))
        audio_data = f[audio_start:audio_end]
        iobytes = io.BytesIO(audio_data)
        # print("iobytes ->", iobytes, type(iobytes))
        waveform, samplerate = sf.read(file=iobytes, dtype='float32')
        # print("waveform, samplerate ->", tensor(waveform), samplerate)
        # audio = AudioSegment.from_raw(iobytes)
        # data, samplerate = sf.read(io.BytesIO(iobytes))
        # print("data, samplerate ->", data, samplerate)
        # audio = Image.open(iobytes)
        # Extract the file name without the path and extension
        file_name = os.path.basename(audio_path)
        file_name_without_extension = os.path.splitext(file_name)[0]

        # Extract the ID and number from the file name
        speaker_id, _, utterance_number = file_name_without_extension.rpartition("_")
        speaker_id = speaker_id.split('_')[0]
        # print("File Name:", file_name)
        # print("ID:", file_id)
        # print("Number at the end:", number)
        # quit()
        # waveforms.append(tensor(waveform))
        # sample_rates.append(samplerate)
        # labels.append(audio_class)
        # speaker_ids.append(speaker_id)
        # utterance_numbers.append(utterance_number)
        waveform = tensor(waveform)
        waveform = waveform.unsqueeze(0)
        return tensor(waveform), samplerate, audio_class, speaker_id, utterance_number
    # return waveforms, sample_rates, labels, speaker_ids, utterance_numbers

class SPEECHCOMMANDS(Dataset):
    """*Speech Commands* :cite:`speechcommandsv2` dataset.

    Args:
        root (str or Path): Path to the directory where the dataset is found or downloaded.
        url (str, optional): The URL to download the dataset from,
            or the type of the dataset to dowload.
            Allowed type values are ``"speech_commands_v0.01"`` and ``"speech_commands_v0.02"``
            (default: ``"speech_commands_v0.02"``)
        folder_in_archive (str, optional):
            The top-level directory of the dataset. (default: ``"SpeechCommands"``)
        download (bool, optional):
            Whether to download the dataset if it is not found at root path. (default: ``False``).
        subset (str or None, optional):
            Select a subset of the dataset [None, "training", "validation", "testing"]. None means
            the whole dataset. "validation" and "testing" are defined in "validation_list.txt" and
            "testing_list.txt", respectively, and "training" is the rest. Details for the files
            "validation_list.txt" and "testing_list.txt" are explained in the README of the dataset
            and in the introduction of Section 7 of the original paper and its reference 12. The
            original paper can be found `here <https://arxiv.org/pdf/1804.03209.pdf>`_. (Default: ``None``)
    """

    def __init__(
        self,
        root: Union[str, Path],
        url: str = URL,
        folder_in_archive: str = FOLDER_IN_ARCHIVE,
        download: bool = False,
        train_path :str = None,
        subset: Optional[str] = None,
    ) -> None:

        if hasattr(self, 'is_mytar') and self.is_mytar:
            print("Using mytar...")
            self.metadata = get_metadata_mytar(self.train_path, self.group_size)
            # print("self.metada ->", self.metadata)
            print("len(self.metadata) ->", len(self.metadata))
        else:
            if subset is not None and subset not in ["training", "validation", "testing"]:
                raise ValueError("When `subset` is not None, it must be one of ['training', 'validation', 'testing'].")

            if url in [
                "speech_commands_v0.01",
                "speech_commands_v0.02",
            ]:
                base_url = "http://download.tensorflow.org/data/"
                ext_archive = ".tar.gz"

                url = os.path.join(base_url, url + ext_archive)

            # Get string representation of 'root' in case Path object is passed
            root = os.fspath(root)
            self._archive = os.path.join(root, folder_in_archive)

            basename = os.path.basename(url)
            archive = os.path.join(root, basename)

            basename = basename.rsplit(".", 2)[0]
            folder_in_archive = os.path.join(folder_in_archive, basename)

            self._path = os.path.join(root, folder_in_archive)

            if download:
                if not os.path.isdir(self._path):
                    if not os.path.isfile(archive):
                        checksum = _CHECKSUMS.get(url, None)
                        download_url_to_file(url, archive, hash_prefix=checksum)
                    _extract_tar(archive, self._path)
            else:
                if not os.path.exists(self._path):
                    raise RuntimeError(
                        f"The path {self._path} doesn't exist. "
                        "Please check the ``root`` path or set `download=True` to download it"
                    )

            if subset == "validation":
                self._walker = _load_list(self._path, "validation_list.txt")
            elif subset == "testing":
                self._walker = _load_list(self._path, "testing_list.txt")
            elif subset == "training":
                excludes = set(_load_list(self._path, "validation_list.txt", "testing_list.txt"))
                walker = sorted(str(p) for p in Path(self._path).glob("*/*.wav"))
                self._walker = [
                    w
                    for w in walker
                    if HASH_DIVIDER in w and EXCEPT_FOLDER not in w and os.path.normpath(w) not in excludes
                ]
            else:
                walker = sorted(str(p) for p in Path(self._path).glob("*/*.wav"))
                self._walker = [w for w in walker if HASH_DIVIDER in w and EXCEPT_FOLDER not in w]

    def get_metadata(self, n: int) -> Tuple[str, int, str, str, int]:
        """Get metadata for the n-th sample from the dataset. Returns filepath instead of waveform,
        but otherwise returns the same fields as :py:func:`__getitem__`.

        Args:
            n (int): The index of the sample to be loaded

        Returns:
            Tuple of the following items;

            str:
                Path to the audio
            int:
                Sample rate
            str:
                Label
            str:
                Speaker ID
            int:
                Utterance number
        """
        fileid = self._walker[n]
        return _get_speechcommands_metadata(fileid, self._archive)

    def __getitem__(self, n: int) -> Tuple[Tensor, int, str, str, int]:
        """Load the n-th sample from the dataset.

        Args:
            n (int): The index of the sample to be loaded

        Returns:
            Tuple of the following items;

            Tensor:
                Waveform
            int:
                Sample rate
            str:
                Label
            str:
                Speaker ID
            int:
                Utterance number
        """
        # print("n --> ", n)
        if self.is_mytar:
            path = self.train_path + '/' + self.metadata[n]['groupname']
            group_metadata = self.metadata[n]['metadata']
            # print("group_metadata ->", group_metadata)
            waveform, sample_rate, label, speaker_id, utterance_number = mytar_loader(path, group_metadata)
            # print("waveform, sample_rate, label, speaker_id, utterance_number ->", tensor(waveform), sample_rate, label, speaker_id, utterance_number)
            return waveform, sample_rate, label, speaker_id, utterance_number
        else:
            metadata = self.get_metadata(n)
            waveform = _load_waveform(self._archive, metadata[0], metadata[1])
            return (waveform,) + metadata[1:]

    def __len__(self) -> int:
        if self.is_mytar:
            print("__len__(self.metadata) ->", len(self.metadata))
            return len(self.metadata)
        else:
            return len(self._walker)