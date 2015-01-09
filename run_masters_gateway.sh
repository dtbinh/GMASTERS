cd `dirname $0`
if [ ! -f masters/MastersServer.class ]; then
    sh build_masters_gateway
fi
java -Djava.library.path=./Netlogo-MASTERS-linux/lib -Dorg.nlogo.is3d=true -cp .:Netlogo-MASTERS-linux/NetLogo.jar:lib/py4j0.8.2.1.jar masters.MastersServer
cd - > /dev/null
