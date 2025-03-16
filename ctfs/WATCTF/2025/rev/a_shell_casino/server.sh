#!/bin/bash

echo 'Welcome to the Bash Casino!'
echo 'Get a score above 1000 and you win our special prize!'

money=5

while [[ 1000 -ge "$money" ]]; do
    echo "You have $money dollars in your account."
    echo 'Flipping a coin...'
    # This would be one-half, but the house needs a cut too...
    flip=$(( RANDOM % 3 == 1 ))
    echo "Do you want to bet 1 dollar on this coin?"
    select yn in "Yes" "No"; do
        case "$yn" in
            No)
                echo "Alright! Let's go again!"
                ;;
            Yes) 
                if [[ 1 -eq "$flip" ]]; then
                    echo "You won! Great job!"
                    money=$(( money + 1 ))
                else
                    echo "You lost. Better luck next time."
                    money=$(( money - 1 ))
                    if [[ 0 -ge "$money" ]]; then
                        echo "You have run out of money :("
                        echo "Sorry, only paying customers are allowed in the casino! Good-bye!"
                        exit
                    fi
                fi
        esac
        break
    done
done

echo "CONGRATS!!!! You are SUPER LUCKY today!"
echo "As a reward, here's our GRAND PRIZE!"
cat /app/flag.txt
