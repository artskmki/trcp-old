#!/bin/bash
host=/localhost/`hostname`.host_cxt

#exit component
rtexit $host/PulseAudioInput0.rtc
rtexit $host/PulseAudioOutput0.rtc
rtexit $host/JuliusRTC0.rtc
rtexit $host/OpenJTalkRTC0.rtc
rtexit $host/FestivalRTC0.rtc
rtexit $host/eSEAT0.rtc
rtexit $host/rosRTMfollowme0.rtc

