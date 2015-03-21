#!/bin/bash
cd ~/catkin_ws/src/trcp/trcp_openhri/scripts 

#start component
pulseaudioinput &
pulseaudiooutput &
openjtalkrtc &
festivalrtc &
juliusrtc followme.xml &
#python ConsoleOut.py &
python rosRTMfollowme.py &
cd ../eSeat
#seat sample.seatml &
python eSEAT.py followme.seatml &

sleep 5; 

#スクリプトからは下記コマンドが無効でした。
#rtcwd 127.0.0.1/

host=/localhost/`hostname`.host_cxt

#active component
rtact $host/PulseAudioInput0.rtc
rtact $host/PulseAudioOutput0.rtc
rtact $host/JuliusRTC0.rtc
rtact $host/OpenJTalkRTC0.rtc
rtact $host/FestivalRTC0.rtc
sleep 5;
rtact $host/eSEAT0.rtc
rtact $host/rosRTMfollowme0.rtc

#connect component
rtcon $host/PulseAudioInput0.rtc:AudioDataOut $host/JuliusRTC0.rtc:data
rtcon $host/JuliusRTC0.rtc:result $host/eSEAT0.rtc:speechin
rtcon $host/eSEAT0.rtc:speechout $host/OpenJTalkRTC0.rtc:text
rtcon $host/eSEAT0.rtc:speechoutE $host/FestivalRTC0.rtc:text
rtcon $host/OpenJTalkRTC0.rtc:result $host/PulseAudioOutput0.rtc:AudioDataIn
rtcon $host/FestivalRTC0.rtc:result $host/PulseAudioOutput0.rtc:AudioDataIn
rtcon $host/eSEAT0.rtc:command $host/rosRTMfollowme0.rtc:input_long
rtcon $host/rosRTMfollowme0.rtc:output_str $host/OpenJTalkRTC0.rtc:text
