FROM python:3.8-alpine

RUN apk update

RUN mkdir /grades_grades_grades
RUN mkdir /grades_grades_grades/src

COPY requirements.txt /grades_grades_grades/
COPY run.py /grades_grades_grades/
COPY run.sh /grades_grades_grades/

COPY ./src /grades_grades_grades/src
RUN chmod +x /grades_grades_grades/run.sh

WORKDIR /grades_grades_grades

CMD ["sh", "run.sh"]
