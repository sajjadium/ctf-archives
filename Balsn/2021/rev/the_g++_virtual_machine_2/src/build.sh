argument=`python3 -c "flag=input();s=(set(flag) - {'{', '}'});import string;assert s.intersection(set(string.ascii_lowercase))==s;print(' '.join([f\"-D__IN_{i}={ ( ord(c)-ord('a') ) % 31 }\" for i, c in enumerate(flag)]))"`
g++ ${argument} -ftemplate-depth=2147483647 -std=c++17 -I. -o output output.cpp

if [ `./output` = "25" ]
then
  echo "yes"
else
  echo "no"
fi

rm output
