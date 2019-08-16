#!/bin/bash

#!/bin/bash

gpio -g mode 21 up
mode=`gpio -g read 21`

if [ $mode == 0 ]; then
    echo "Use ELM Emulator"

    cd $HOME/ELM327-emulator
    echo -e 'scenario car\n"RUNNING"' | /usr/bin/python3 -m elm -b $HOME/testlog.out &

    sleep 1

    export OBDPORT=`head -n 1  $HOME/testlog.out`

else
    echo "Use TTY"
    export OBDPORT=/dev/ttyUSB0
fi


echo "SET OBDPORT to $OBDPORT"

while ! /sbin/ifconfig | grep "inet 192.168.4.1" > /dev/null; do
	echo "Waiting for wifi ap... "
	sleep 1
done


cd $HOME/obd2mqtt
/usr/bin/python3 obd_gateway.py > $HOME/tester.log &
sleep 5
/usr/bin/python3 mq_mon.py > $HOME/mq_mon.log &
