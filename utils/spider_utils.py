# -*- coding: utf-8 -*-
import sys
import time
import requests

def download_file(url, filename, chunk_size=1024):
    """
    可以下载各种文件，包括视频，chunk_size可以控制写入速度
    """
    start_time = time.time()
    with requests.get(url, stream=True, verify = False) as rsp:
        if rsp.status_code != 200:
            sys.stderr.write("error, code={code}, msg={msg}\n".format(code=rsp.status_code, msg=rsp.text))
            return

        content_size = int(rsp.headers['Content-Length'])
        file_size = content_size / (1024 * 1024.0)
        sys.stderr.write("url: {url}\n".format(url=url))
        sys.stderr.write("文件大小: {:.2f} Mb\n".format(file_size))

        with open(filename, "wb") as f:
            idx, offset, cur_bytes = 0, 0, 0
            st = time.time()
            for data in rsp.iter_content(chunk_size=chunk_size):
                f.write(data)
                num = len(data)
                offset += num
                cur_bytes += num

                if idx % 100 == 0:
                    cur_time = time.time()
                    et = cur_time
                    time_cost = et - st

                    # Mb/s
                    speed = (cur_bytes/(1024.0 * 1024)) / max(time_cost, 0.0001)
                    percent = int((offset + 0.0) / content_size * 100 + 0.5)
                    tag = "=" * percent

                    cur_time_cost = cur_time - start_time
                    cur_size = offset / (1024.0 * 1024.0)

                    msg = ("\r[下载进度]: {tag} {percent}% {cur_time_cost:.2f}s" +
                            " {cur_size:.2f}Mb {speed:.3f}Mb/s ").format(tag=tag, percent=percent, \
                            cur_time_cost=cur_time_cost, cur_size=cur_size, speed=speed)
                    sys.stderr.write(msg)
                    # 重置计数器
                    idx, st, cur_bytes = 0, et, 0

                idx += 1
        sys.stderr.write('\n')

if __name__ == '__main__':
    url = 'https://video.study.163.com/edu-video/nos/mp4/2017/08/28/1006903016_2a313fb0cbfc43c1aac97c5692075bf4_sd.mp4?ak=7909bff134372bffca53cdc2c17adc27a4c38c6336120510aea1ae1790819de846ef9a86dc8c1bfdf2bcf0e4ca642af89f4f2c365f921025e6f7c7879d5b3c043059f726dc7bb86b92adbc3d5b34b132f3e000b69b31389b18d43e4d925b69224cca709eeec35724f15d3e6a182e04cb'
    download_file(url, "test.mp4")
