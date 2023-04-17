# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/4/7 15:51
# Desc: 机器人播放音频文件。

from utils.ssh_linux import MySSH
from time import sleep


def palyAudio(host, audio_file='StopLongTime.wav', volume=100, count=3):
    """
    :param host:  需要控制的机器人。
    :param audio_file:  需要播放的异常音频文件。
    :param volume:  播放音频使用的扬声器音量值。
    :param count:  播放几次。
    :return:  None
    """
    ssh = MySSH(host)
    ssh.exe_cmd(f"amixer cset numid=864,iface=MIXER,name='x Speaker Playback Volume' {volume}%")  # 先调节音量
    if ssh.exe_cmd(f"ls -l ~/audio/{audio_file}"):
        pass
    else:
        ssh.scp_file(file=f"./config_file/audio.tar.gz", path='~/')
        ssh.exe_cmd(f"tar -xzf audio.tar.gz")
    for i in range(count):
        ssh.exe_cmd(f"aplay ~/audio/{audio_file}")  # 播放音频
        sleep(3)
    ssh.exe_cmd("amixer cset numid=864,iface=MIXER,name='x Speaker Playback Volume' 10%")  # 恢复扬声器音量。


if __name__ == '__main__':
    palyAudio('10.2.9.125')
