The math exam starts now. Participate with integrity and never cheat.

Someone has stolen the exam paper, and definitely he got full marks.
Fortunately, he didn't find the flag.

#!/bin/bash

echo "You are now in the math examination hall."
echo "First, please read exam integrity statement:"
echo ""

promisetext="I promise to play fairly and not to cheat. In case of violation, I voluntarily accept punishment"
echo "$promisetext"
echo ""

echo "Now, write down the exam integrity statement here:"
read userinput

if [ "$userinput" = "$promisetext" ]
then
    echo "All right"
else
    echo "Error"
    exit
fi

echo ""
echo "Exam starts"
echo "(notice: numbers in dec, oct or hex format are all accepted)"
echo ""

correctcount=0
for i in {1..100}
do
    echo "Problem $i of 100:"
    echo "$i + $i = ?"

    ans=$(($i+$i))
    read line

    if [[ "$line" -eq "$ans" ]]
    then
        correctcount="$(($correctcount+1))"
    fi
    echo ""
done

echo "Exam finishes"
echo "You score is: $correctcount"

exit
