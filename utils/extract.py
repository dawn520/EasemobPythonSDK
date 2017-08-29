import tarfile


def extract(tar_path, target_path):
        # tar = tarfile.open(tar_path, "r:gz")
        # file_names = tar.getnames()
        # for file_name in file_names:
        #     tar.extract(file_name, target_path)
        # tar.close()
        tar = tarfile.open(tar_path)
        tar.extractall()
        tar.close()


# extract('../2017072410.gz', './')
