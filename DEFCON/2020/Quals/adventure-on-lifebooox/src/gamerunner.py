#! /usr/bin/env python3
import lifebox_task
import rq.registry
import statistics
import traceback
import signal
import select
import shutil
import redis
import json
import time
import uuid
import sys
import os
import re
import rq


DEBUG=1

RESULTS_LOG = ""
BASE_DIR = ""
NUMBER_OF_WORKERS = ""

def get_pattern():
    print("Please paste pattern followed by a newline:")
    sys.stdout.flush()
    pattern_lines = ""
    for line in sys.stdin:
        pattern_lines += line
        if line.strip() == "":
            break
        assert len(pattern_lines) < (1024*1024), "Pattern too long"
    assert len(pattern_lines) > 1, "Pattern too short to be a valid submission"

    regex_first_line = r"^x = [\-0-9]{1,5}, y = [\-0-9]{1,5}"
    regex_other_line = r"^[!$.0-9A-G]*$"

    for index, line in enumerate(pattern_lines.split("\n")):
        if index==0:
            assert re.match(regex_first_line, line), "The uploaded format is not correct"
        else:
            if not line.startswith("#"):
                assert re.match(regex_other_line, line), "The uploaded format is not correct"

    print(f"Received pattern of {len(pattern_lines)} bytes.")
    sys.stdout.flush()
    return pattern_lines


def job_monitor(job, q):

    last_results_len = 0
    loop_cnt = 0
    time.sleep(2)  # give it a chance to startup everything

    while True:

        results = open(RESULTS_LOG).read()
        res_lines = results.split("\n")
        current_res_len = len(res_lines)

        # print only the new information
        if last_results_len < current_res_len:
            for i in range(last_results_len - 1, current_res_len):
                out_line = res_lines[i].strip()
                if len(out_line) > 0:
                    sys.stdout.write(f"{out_line}\n")
                    sys.stdout.flush()

            last_results_len = current_res_len

        if job.get_status() == "queued" and loop_cnt % 5 == 0:
            print(f"Waiting for position, a total of {q.count} jobs in the queue")
            sys.stdout.flush()

        if results.find("WINNER") > -1 or results.find("GAME OVER") > -1 or results.find("#100") > -1:
            while job.get_status() != "finished" and job.get_status() != "failed":
                print(f" waiting for job status, which is currently {job.get_status()}")
                time.sleep(1)

            if results.find("WINNER") > -1:
                print("\n")
                print(open("/flag").read())
                print("\n")
                sys.stdout.flush()

                break

            if results.find("GAME OVER") > -1:
                break

            if results.find("#100") > -1:
                print("100 million steps exceeded, ending trial.")
                sys.stdout.flush()
                break

        time.sleep(3)
        if job.get_status() == "failed":
            print("Exiting due to job failure..")
            sys.stdout.flush()

            break
        loop_cnt += 1
    print("Done running golly.")


def get_extra_cfg(pow_levels, pow_n, min_time):
    try:
        if os.path.exists("/tmp/config.json"):
            with open("/tmp/config.json","r") as jfile:
                jdata = json.load(jfile)

            if "POW_LEVELS" in jdata:
                print("found levels")
                pow_levels = int(jdata["POW_LEVELS"])
            if "POW_N" in jdata:
                pow_n = int(jdata["POW_N"])
            if "MIN_TIME" in jdata:
                min_time = int(jdata["MIN_TIME"])
        if "POW_LEVELS" in os.environ:
            pow_levels = int(os.getenv("POW_LEVELS"))
        if "POW_N" in os.environ:
            pow_n = int(os.getenv("POW_N"))
        if "MIN_TIME" in os.environ:
            min_time = int(os.getenv("MIN_TIME"))

    except Exception as ex:
        print("ERROR " * 20)
        print(ex)
        sys.stdout.flush()
        pass

    return pow_levels, pow_n, min_time


def main():
    global BASE_DIR, RESULTS_LOG
    job = None

    finished_run_times = []

    try:

        rq.use_connection(redis.Redis())
        q = rq.Queue("lifeboxQueue")
        for jid in q.finished_job_registry.get_job_ids():
            fj = q.fetch_job(jid)
            delta = fj.ended_at - fj.started_at
            finished_run_times.append(delta.seconds)

        if q.count == 0:
            print(f"Welcome to LIFEBOX online")
        else:
            registry = rq.registry.StartedJobRegistry('default')
            number_jobs = len(q.started_job_registry.get_job_ids())
            if len(finished_run_times) > 0:
                estimated_time = (q.count / number_jobs) * statistics.mean(finished_run_times)
            else:
                estimated_time = (q.count / number_jobs) * 720
            print(f"Welcome to LIFEBOX online.\n\tWe have {q.count} players currently waiting in the queue and {number_jobs} being processed (Est hold time is {estimated_time:.0f} seconds)")

        os.chdir(os.sep)

        attempt_id = str(uuid.uuid4())
        while os.path.exists(os.path.join(str(os.sep), "tmp", attempt_id)):
            attempt_id = str(uuid.uuid4())

        BASE_DIR = os.path.join(str(os.sep), "tmp", attempt_id)
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)

        RESULTS_LOG = os.path.join(BASE_DIR, "results.log")

        pattern_lines = get_pattern()

        open(os.path.join(BASE_DIR,"pattern.dat"),"w").write(pattern_lines)

        open(RESULTS_LOG, "w").write("Pattern saved, adding job to Queue\n")

        job = q.enqueue(lifebox_task.start, attempt_id, RESULTS_LOG, job_timeout=60*15, job_id=attempt_id, result_ttl=60*60*48)

        job_monitor(job, q)

    except KeyboardInterrupt:
        print("Keyboard interrupt...")
    except Exception as ex:
        errstr = traceback.format_exc()
        print(f"\033[38;5;9m{errstr}\033[0m")
    finally:
        # job cleanup
        if job is not None:
            if job.get_status() == "failed":
                print("Process was aborted for some reason")
            elif job.get_status() == "finished":
                print("Process completed")
            else:
                if os.path.exists(RESULTS_LOG):
                    open(RESULTS_LOG, "a").write("\nGAME OVER\n")
                print(f"Cancelling job {job.key}")
                job.cancel()

        #shutil.rmtree(BASE_DIR, ignore_errors=True)

if __name__ == '__main__':
    main()