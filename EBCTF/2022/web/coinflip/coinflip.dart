import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:convert/convert.dart';
import 'package:shelf_router/shelf_router.dart';
import 'package:shelf/shelf.dart';
import 'package:shelf/shelf_io.dart' as io;
import 'package:shelf_secure_cookie/shelf_secure_cookie.dart';

const maxGuesses = 30;
const Duration sessionTimeout = Duration(seconds: 180);
const Duration cleanInterval = Duration(seconds: 10);

List<int> rand(n) {
  var l = <int>[];

  for(var i = 0; i < n; i++) {
    l.add(random.nextInt(256));
  }

  return l;
}

class Session {
  String id;

  int timesPlayed;
  int timesWon;

  final DateTime timeCreated = DateTime.now();

  Session({this.timesPlayed = 0, this.timesWon = 0, required this.id});

  static Session create() {
    final buffer = rand(16);
    final h = hex.encode(buffer);
    return Session(id: h);
  }

  @override
  String toString() {
    return 'id=$id timesPlayed=$timesPlayed timesWon=$timesWon';
  }
}

class SessionStore {
  final sessionStore = <String, Session>{};

  int cleanup() {
    var n = sessionStore.length;

    sessionStore.removeWhere((key, value) => DateTime.now().difference(value.timeCreated).compareTo(sessionTimeout) > 0);

    return (n - sessionStore.length);
  }

  String add(Session s) {
    sessionStore[s.id] = s;
    return s.id;
  }

  bool remove(Session s) {
    if(sessionStore.containsKey(s.id)) {
      return sessionStore.remove(s.id) != null;
    }

    return false;
  }

  Session? get(String sid) {
    if(sessionStore.containsKey(sid)) {
      return sessionStore[sid];
    }

    return null;
  }
}

Session loadSession(Request request) {
  CookieParser cookies = request.context['cookies'] as CookieParser;
  Cookie? sessionId = cookies.get('sid');

  Session? s;

  if(sessionId != null) {
    s = sessionStore.get(sessionId.value.toLowerCase());
  }

  if(s == null) {
    s = Session.create();
    final sid = sessionStore.add(s);
    cookies.set('sid', sid);
  }

  return (Session.create())
    ..id = s.id
    ..timesPlayed = s.timesPlayed
    ..timesWon = s.timesWon;
}

bool coinFlip() {
  return random.nextInt(2).isEven;
}

Random random = Random.secure();
late SessionStore sessionStore;

void main(List<String> arguments) async {
  final flag = Platform.environment['FLAG'];
  if(flag == null) {
    print('flag missing');
    exit(1);
  }

  sessionStore = SessionStore();

  ProcessSignal.sigint.watch().forEach((element) => exit(0));

  Timer.periodic(cleanInterval, (t) {
    final n = sessionStore.cleanup();
    if(n > 0) {
      //print('removed $n sessions');
    }
  });

  var app = Router();

  app.post('/flip', (Request request) async {
    final session = loadSession(request);
    var guess = false;
    String body;

    body = await request.readAsString();

    switch(body) {
      case 'heads':
        guess = true;
        break;
      case 'tails':
        guess = false;
        break;
      default:
        return Response.badRequest(body: 'Bad request. Send "heads" or "tails"');
    }

    final flip = coinFlip();

    session.timesPlayed++;

    final result = guess == flip;

    if(result) {
      session.timesWon++;
    }

    final gameOver = session.timesPlayed >= maxGuesses;

    if(gameOver) {
      sessionStore.remove(session);
    } else {
      sessionStore.add(session);
    }

    var response = <String, dynamic>{
      'correct': result,
      'timesPlayed': session.timesPlayed,
      'timesWon': session.timesWon,
      'gameOver': gameOver,
    };

    if(session.timesWon >= maxGuesses) {
      response['flag'] = flag;
    }

    final headers = gameOver ? {HttpHeaders.setCookieHeader: (request.context['cookies'] as CookieParser).toHeader()} : null;

    return Response.ok(json.encode(response), headers: headers);
  });

  app.get('/', (Request request) {
    return Response.ok('Welcome to the MCH coin flip service. Post your guess ("heads" or "tails") to /flip. Win $maxGuesses times in a row to claim the prize.');
  });

  final pipeline = Pipeline()
      .addMiddleware(cookieParser())
      .addHandler(app);

  await io.serve(pipeline, '0.0.0.0', 8080);
}
