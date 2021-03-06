# Carmen Sandiego Handout

Carmen isn't your average thief – in fact, she's trying to save the artifacts she steals! Join Carmen, Player, Zach, and Ivy as they protect the world's cultural history from the likes of VILE, one theft at a time. But they have to be careful: ACME thinks they're on the wrong side of the law and will stop at nothing to bring them to justice.

## Important Hint

The intended solution uses a bug in `file.c` of GoAhead.  (Feel free to look for bugs elsewhere though!)

## Description

`frontend` - The web interface for launching a new instance.  This is part of the challenge infrastructure, and we're only providing it to you so that you can have an accurate testing environment.  It is considered out of scope for the problem; please don't attack it.  Do let bluepichu know if you have any issues though.

`instance` - The actual instance (IoT hub + victim) that gets launched when you create a job.

## Deploy

To deploy:

1. In `instance`, run `docker-compose build` (see `docker-compose.override.yml` for switching between the two parts of the problem)
2. In `frontend`, run `docker-compose up`

You can also run `docker-compose up server` in `instance` to launch a single persistent instance.  If you do this, set `SENSOR_TOKEN` and `ADMIN_PASSWORD` appropriately so you can authenticate.
