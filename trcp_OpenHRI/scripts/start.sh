#!/bin/bash

#cd /home/ito/Dropbox/Programing/workspace/121104_consoleIn/src
cd ~/catkin_ws/src/trcp/trcp_OpenHRI/scripts 

#start component
pulseaudioinput &
pulseaudiooutput &
openjtalkrtc &
juliusrtc sample.xml &
#python ConsoleOut.py &
cd ../eSeat
#seat sample.seatml &
python eSEAT.py a.seatml &
sleep 10;

#スクリプトからは下記コマンドが無効でした。
#rtcwd 127.0.0.1/

#active component
rtact 127.0.0.1/M14xR2.host_cxt/PulseAudioInput0.rtc
rtact 127.0.0.1/M14xR2.host_cxt/JuliusRTC0.rtc
rtact 127.0.0.1/M14xR2.host_cxt/eSEAT0.rtc
rtact 127.0.0.1/M14xR2.host_cxt/OpenJTalkRTC0.rtc
rtact 127.0.0.1/M14xR2.host_cxt/PulseAudioOutput0.rtc

#connect component
rtcon 127.0.0.1/M14xR2.host_cxt/PulseAudioInput0.rtc:AudioDataOut 127.0.0.1/M14xR2.host_cxt/JuliusRTC0.rtc:data
rtcon 127.0.0.1/M14xR2.host_cxt/JuliusRTC0.rtc:result 127.0.0.1/M14xR2.host_cxt/eSEAT0.rtc:speechin
rtcon 127.1.0.1/M14xR2.host_cxt/eSEAT0.rtc:speechout 127.0.0.1/M14xR2.host_cxt/OpenJTalkRTC0.rtc:text
rtcon 127.0.0.1/M14xR2.host_cxt/OpenJTalkRTC0.rtc:result 127.0.0.1/M14xR2.host_cxt/PulseAudioOutput0.rtc:AudioDataIn

