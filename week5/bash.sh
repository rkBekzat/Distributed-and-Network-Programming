list=$(ps -xal | grep 10900 | grep do_sys | awk '{print $3}')


echo "these processes are found"
echo $list

for var in $list; do
	echo "Killing $var"
	$(kill -KILL $var)
done
