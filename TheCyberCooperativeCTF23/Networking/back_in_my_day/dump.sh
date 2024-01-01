REFF=/tmp/.streams
echo "" > $REFF
mkdir streams
while true 
do
tshark -r $@ -T fields -e tcp.stream 2> /dev/null | sort -nu | sed '/^$/d' | while read i
do
    if [ -z "$(cat $REFF | grep "^$i$" )" ]
    then
          tshark -r $@ -qz follow,tcp,ascii,$i  | tee ./streams/${@}-stream-$i.txt
          echo $i >> $REFF
    fi
done
done
