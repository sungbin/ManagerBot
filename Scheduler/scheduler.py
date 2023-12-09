import json
import os
import subprocess
import threading
import time

def run_job(job, continue_event):
    while True:
        while not job['continue']:
            print(f"Job {job['target']} is set to not continue.")
            continue_event.wait()
            continue_event.clear()
    
        print(f"Starting job: {job['target']}")
    
        while job['continue']:
            process = subprocess.Popen(
                [job['runner'], job['target']],
                cwd=job['cwd'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            _, _ = process.communicate()
            time.sleep(job['interval'])
    
        print(f"Job {job['target']} stopped.")

def update_json_file(jobs):
    with open('schedule.json', 'w') as file:
        json.dump(jobs, file, indent=2)

def main_logic(jobs, continue_events):
    while True:
        # 파이프 입력 확인
        fifo_path = "../Pipes/to_scheduler"
        with open(fifo_path, "rb") as fifo:
            pipe_data = fifo.read(2)
            print(f"Received - {pipe_data}")

        if pipe_data:
            command, index = pipe_data[0], pipe_data[1]

            key = list(jobs.keys())[index]
            continue_event = continue_events[key]

            if command == 1:
                # continue 값을 true로 변경 (command=1)
                jobs[key]['continue'] = True
                continue_event.set()  # 해당 이벤트를 설정하여 실행을 시작
                print("set True", key)
            elif command == 2:
                # continue 값을 false로 변경 (command=2)
                print("set False", key)
                jobs[key]['continue'] = False
            else:
                print("Invalid command.")

                # 업데이트된 jobs를 JSON 파일에 저장
            update_json_file(jobs)

def main():
    with open('schedule.json', 'r') as file:
        jobs = json.load(file)

    # 각 job에 대한 이벤트를 만듦
    continue_events = {key: threading.Event() for key in jobs.keys()}

    # 각 job을 별도의 스레드로 실행
    job_threads = [threading.Thread(target=run_job, args=(job, continue_events[key])) for key, job in jobs.items()]

    for thread in job_threads:
        thread.start()

    try:
        while True:
            main_logic(jobs, continue_events)
    except KeyboardInterrupt:
        pass
    finally:
        # 프로그램 종료 시 각 job 스레드를 기다림
        for thread in job_threads:
            thread.join()

if __name__ == "__main__":
    main()
