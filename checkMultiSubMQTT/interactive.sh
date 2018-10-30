#!/bin/sh

echo "What are you going to do?"
echo "(1)submultitopic"
echo "(2)submultitopics"
echo "(3)pubmultitopics"


function submt() {
read -p 'amount: ' amount
read -p 'qos: ' qos
read -p 'topic: ' topic

./submultitopic.sh $amount $qos $topic
}

function submts() {
echo 'topic: test/{1....$amount}'
read -p 'amount: ' amount
read -p 'qos: ' qos
./submultitopics.sh $amount $qos
}

function pubmulti() {
echo 'topic: test/{1....$amount}'
echo 'amount should as same as option 2 entered'
read -p 'amount: ' amount
read -p 'qos: ' qos

./pubmultitopic.sh $amount $qos
}
read choice

case $choice in

    1)
        submt; echo 'done!'    # Do Stuff
        ;;
    2)
        submts; echo 'done!'  # Do different stuff
        ;;
    3)
        pubmulti; echo 'done!'  # Do different stuff
        ;;
    *)
        echo $choice 'is not a valid choice'
        ;;
esac
