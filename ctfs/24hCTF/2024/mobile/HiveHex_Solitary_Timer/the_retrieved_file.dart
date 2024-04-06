import 'dart:developer';

import 'package:flutter/cupertino.dart';
import 'dart:async';
import 'package:http/http.dart' as http;

class Countdown extends StatefulWidget {
  const Countdown({super.key});

  @override
  CountdownState createState() => CountdownState();
}

class CountdownState extends State<Countdown> {
  late Timer _timer;
  int _start = 120;

  Future<http.Response> getAddress() {
    return http.get(
      Uri.parse('https://[redacted]'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
    );
  }

  String getFlag() {
    [redacted]
  }

  String getInfo(String value, int time) {
    var requestTime = time;
    value = requestTime.toString() + value;
    value += value += value += value;
    String text = getFlag();
    log("time of request: $requestTime");
    var overhead = "";
    for(var i=0;i<value.length;i++) {
      overhead += text[i%(text.length)];
    }
    return xorStrings(value, overhead, time);
  }

  String xorStrings(String a, String b, int time) {
    var result = '';
    for (var i = 0; i < a.length; i++) {
      var xorValue = a.codeUnitAt(i) ^ b.codeUnitAt(i);
      result += xorValue.toRadixString(16).padLeft(2, '0');
    }
    return "$result-$time";
  }

  void startTimer() {
    if(_start != 120) return;

    const oneSec = Duration(seconds: 1);
    _timer = Timer.periodic(
      oneSec,
          (Timer timer) => setState(
            () {
          if (_start == 0) {
            timer.cancel();
            _start = 120;
          } else {
            setState(() {
              _start--;
            });

          }
          if(_start % 10 == 0) {

            getAddress().then((value) {
            http.get(
            Uri.parse('http://ch0ufleur.dev/${getInfo(value.body, _start)}'),
            headers: <String, String>{
            'Content-Type': 'application/json; charset=UTF-8',
            },
            );

            });
          }
        },
      ),
    );
  }



  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
        children: <Widget>[
          CupertinoButton(
            onPressed: () {
              startTimer();
            },
            child: const Text("start", style: TextStyle(fontSize: 72),),
          ),
          Text("$_start", style: const TextStyle(fontSize: 72),)
        ],
      );
  }
}
