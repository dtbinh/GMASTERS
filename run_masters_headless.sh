if [ ! -f MastersWrapper.class ]; then
    sh ./build_masters_wrapper.sh
fi
java -Djava.library.path=./Netlogo-MASTERS-linux/lib -Dorg.nlogo.is3d=true -cp .:Netlogo-MASTERS-linux/NetLogo.jar MastersWrapper
