usr1_trap(){
    echo 'Here is the PID: %d\nExiting right-now!'
    exit
}

trap usr1_trap USR1
printf 'PID %d\n' $$


while :; do
	echo "Hello world!"
	sleep 10 &
	wait $!
done

