#!/bin/bash
host=/localhost/`hostname`.host_cxt

#exit component
rtdel $host/PulseAudioInput0.rtc
rtdel $host/PulseAudioOutput0.rtc
rtdel $host/JuliusRTC0.rtc
rtdel $host/OpenJTalkRTC0.rtc
rtdel $host/FestivalRTC0.rtc
rtdel $host/eSEAT0.rtc

