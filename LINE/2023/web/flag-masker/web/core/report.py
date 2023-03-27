from redis import Redis

class Report:
  def __init__(self):
    try:
      self.conn = Redis(host="redis", port=6379)

    except Exception as error:
      print(error, flush=True)

  def submit(self, data: object):
    try:
      self.conn.lpush("query", data["url"])

    except Exception as error:
      print(error, flush=True)