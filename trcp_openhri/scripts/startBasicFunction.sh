#!/bin/bash
cd ~/catkin_ws/src/trcp/trcp_openhri/scripts 

#start component
pulseaudioinput &
pulseaudiooutput &
echosuppressor &
#echocanceler &
openjtalkrtc &
festivalrtc &
juliusrtc basicfunction.xml &
python rosRTMbasicfunction.py &
(cd ../eSeat; ./eSEAT.py basicfunction.seatml)&

sleep 5; 

#スクリプトからは下記コマンドが無効でした。
#rtcwd 127.0.0.1/

host=/localhost/`hostname`.host_cxt

#active component
rtact $host/PulseAudioInput0.rtc
rtact $host/PulseAudioOutput0.rtc
rtact $host/EchoSuppressor0.rtc
#rtact $host/EchoCanceler0.rtc
rtact $host/JuliusRTC0.rtc
rtact $host/OpenJTalkRTC0.rtc
rtact $host/FestivalRTC0.rtc
sleep 5;
rtact $host/rosRTMbasicfunction0.rtc

#connect component
rtcon $host/PulseAudioInput0.rtc:AudioDataOut $host/EchoSuppressor0.rtc:AudioDataIn
#rtcon $host/PulseAudioInput0.rtc:AudioDataOut $host/EchoCanceler0.rtc:AudioDataIn
rtcon $host/EchoSuppressor0.rtc:AudioDataOut $host/JuliusRTC0.rtc:data
rtcon $host/EchoSuppressor0.rtc:ReferenceAudioDataIn $host/PulseAudioOutput0.rtc:AudioDataOut
#rtcon $host/EchoCanceler0.rtc:AudioDataOut $host/JuliusRTC0.rtc:data
#rtcon $host/EchoCanceler0.rtc:ReferenceAudioDataIn $host/PulseAudioOutput0.rtc:AudioDataOut

rtcon $host/JuliusRTC0.rtc:result $host/eSEAT0.rtc:speechin
rtcon $host/eSEAT0.rtc:speechout $host/OpenJTalkRTC0.rtc:text
rtcon $host/eSEAT0.rtc:speechoutE $host/FestivalRTC0.rtc:text
rtcon $host/OpenJTalkRTC0.rtc:result $host/PulseAudioOutput0.rtc:AudioDataIn
rtcon $host/FestivalRTC0.rtc:result $host/PulseAudioOutput0.rtc:AudioDataIn
rtcon $host/eSEAT0.rtc:command $host/rosRTMbasicfunction0.rtc:input_long
rtcon $host/eSEAT0.rtc:qa $host/rosRTMbasicfunction0.rtc:qa_long
rtcon $host/rosRTMbasicfunction0.rtc:output_str $host/OpenJTalkRTC0.rtc:text


sleep 5;
rtact $host/eSEAT0.rtc
