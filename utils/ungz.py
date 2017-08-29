import gzip
import os


def un_gz(file_name, mode=0):
    """ungz zip file"""
    f_name = file_name.replace(".gz", "")
    # 获取文件的名称，去掉
    g_file = gzip.GzipFile(file_name, 'rb')
    result = g_file.readlines()
    # 创建gzip对象
    if mode == 1:
        open(f_name, "w+").write(result)
        result = True
    # gzip对象用read()打开后，写入open()建立的文件中。
    g_file.close()
    # 关闭gzip对象
    return result
