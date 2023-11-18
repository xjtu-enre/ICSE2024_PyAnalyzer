'''
This script aims to run automated usability test on selected dependency exraction tools.

This script depends on:
    Git (through environment path)
    SciTools Understand (through environment path)
    SourceTrail (through environment path)
    Java >= 15 (through environment path)
    Python >= 3.8 (through environment path)

    pip install psutil // For memory usage monitoring
    pip install pyuserinput // For automate SourceTrail

This script has only been tested on Windows 10/11.
'''

import re
import io
import logging
import signal
from os import path, rename
import sys
import csv
import subprocess
import time
import argparse
from datetime import datetime
from threading import Timer, Thread
from functools import reduce
import os

def get_files(target_dir):
	global py_list
	for filename in os.listdir(target_dir):
		filepath = os.path.join(target_dir, filename)
		if os.path.isdir(filepath):
			get_files(filepath)
		elif os.path.isfile(filepath) and filename.endswith(".py"):
			py_list.append(filepath)

timestamp = datetime.now().strftime("%y%m%d%H%M")

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler(
            f'./logs/{timestamp}.log'),
        logging.StreamHandler()
    ]
)

try:
    import psutil
except NameError:
    logging.warning('Can not import psutil, memory usage monitoring disabled')


def memory_profiling(pid):
    value = {'peak': -1}

    def task(pid, value):
        if psutil is None:
            value['peak'] = -1
            return value

        while True:
            prev = value['peak']
            try:
                psection = True
                me = psutil.Process(pid)
                curr = me.memory_info().rss
                psection = False
                # Also counting descendents
                children = me.children(recursive=True)
                curr += reduce(lambda p, v: p + v,
                               map(lambda sp: sp.memory_info().rss, children), 0)
                # Convert unit from B to MB
                curr /= 1024 ** 2
            except (psutil.ProcessLookupError, psutil.NoSuchProcess):
                if psection is True:
                    # This usually happens after the process is finished/killed but the function is still invoked
                    logging.warning(
                        f'Losing process with pid={pid}')
                    # By breaking the loop, this thread should be terminated
                    break
                else:
                    # Suppress the losing of subprocesses
                    pass
            else:
                value['peak'] = curr if curr > prev else prev

                # pyanalyzer-python has a memory leak bug if running in Windows 11 (not sure)
                # so in general, if a process is taking too much memory,
                # then we just kill it and let latter projects be run.
                #
                # Current threshold is 20GB
                if value['peak'] > 1024 * 20:
                    for c in children:
                        c.kill()
                    me.kill()
                    value['peak'] = 0
                    logging.warning(
                        f'The process with pid={pid} took too much memory and thus been killed')
                    break

                # Set interval to 0.5 for the tradeoff between accuracy and performance
                # (busy loop will cause the target process to be extremely slow, which
                # should definitely not be used)
                time.sleep(0.5)

    Thread(target=task, args=(pid, value,)).start()
    return value


# Usage
parser = argparse.ArgumentParser()
parser.add_argument('lang', help='Sepcify the target language')
parser.add_argument('range', help='Specify the start line from csv file')
parser.add_argument('only', help='Specify the only tool to run', nargs='?')
parser.add_argument('-t',
                    '--timeout',
                    help='Specify the maximum duration of a single process',
                    type=int)
args = parser.parse_args()

lang = args.lang

range = args.range.split('-')
if len(range) == 1:
    from_line = int(range[0])
    end_line = int(range[0])
elif len(range) == 2:
    from_line = int(range[0])
    end_line = int(range[1])
else:
    raise ValueError(
        f'Invalid range format {args.range}, only support x or x-x')

only = args.only.lower() if args.only is not None else ''
try:
    ['clone', 'loc', 'depends', 'pysonar2', 'pycg', 'enre19',
        'understand', 'sourcetrail',, 'pyanalyzer', ''].index(only)
except ValueError:
    raise ValueError(
        f'Invalid tool {only}, only support depends / pyanalyzer / understand / sourcetrail / clone / loc / PySonar2 / enre19 / PyCG')

# Feature set
timeout = args.timeout  # None, or positive int
if timeout is not None:
    if timeout < 0 or timeout > 3600:
        raise ValueError(
            f'Invalid timeout value {timeout}, only range(300, 3600) are valid')
    if timeout < 300:
        logging.warning(
            f'Unrecommended timeout value {timeout}, this value is too low to get useful information, and is allowed only for debug purpose')

logging.info(
    f'Working on {from_line}-{end_line} for {lang}'
    + f' with {"all tools" if only == "" else f"{only} only"}'
    + (f' and timeout limit to {timeout}' if timeout is not None else ''))

outfile_path = f'./records/{timestamp}-{lang}-{from_line}-{end_line}.csv'

with open(f'{outfile_path}.pending', 'a+') as f:
    f.write(
        'project_name'
        + ',LoC'
        + ',Depends-time'
        + ',Depends-memory'
        + ',SourceTrail-time'
        + ',SourceTrail-memory'
        + ',Understand-time'
        + ',Understand-memory'
        + ',PySonar2-time'
        + ',PySonar2-memory'
        + ',PyCG-time'
        + ',PyCG-memory'
        + ',ENRE19-time'
        + ',ENRE19-memory'
        + ',pyanalyzer-time'
        + ',pyanalyzer-memory'
        + '\n')

project_clone_url_list = dict()
try:
    with open(f'./lists/python_project_list.csv', 'r', encoding='latin-1') as file:
        project_list = csv.reader(file)
        count = 0
        for row in project_list:
            if (count >= from_line) and (count <= end_line):
                project_name = row[0]
                project_clone_url_list[project_name] = count
            count += 1
except EnvironmentError:
    logging.error(f'Can not find project list for {args.lang}')
    sys.exit()

# Cloning (or reusing) repository from GitHub
for project_name in project_clone_url_list.keys():
    print(project_name)
    repo_path = f'./repo/{project_name}'
    from pathlib import Path

    abs_repo_path = Path(str(path.dirname(__file__)) + str(f'\\repo\{project_name}'))
    logging.info(
        f'Reusing existed local repository for {project_name}')
    records = dict()
    # Obtain LoC (only when process all tools)
    if only == 'loc' or only == '':
        print('Counting line of code')
        LoC = 0
        cmd = f'.\\utils\\cloc-1.92.exe {repo_path} --csv --quiet'
        try:
            # A fixed timeout threshold is only activated on process all,
            # which allow LoC counting to exeed the time when only process LoC
            proc = subprocess.check_output(
                cmd, timeout=180 if only == '' else None)
        except subprocess.TimeoutExpired:
            logging.exception(
                f'Counting LoC for {project_name} timed out')
            records['LoC'] = -1
        except subprocess.CalledProcessError:
            logging.exception(
                f'Failed couting line of code for {project_name}')
            records['LoC'] = -1
        else:
            outs = proc.strip().decode('utf-8').splitlines()
            for out in outs:
                out = out.split(',')
                if len(out) == 5:
                    if out[1] == 'Python':
                        LoC += int(out[-1])
            logging.info(f'LoC for {project_name} is {LoC}')
        records['LoC'] = LoC
    else:
        records['LoC'] = 0

    # Run pyanalyzer
    if only == 'pyanalyzer' or only == '':
        print('Starting pyanalyzer')
        cmd = f'{path.join(path.dirname(__file__), "./tools/pyanalyzer/pyanalyzer.exe")} {abs_repo_path} --cfg --cg'
        print(cmd)

        # Whether placing the start of timer here or after the creation
        # has no significant impact on the final duration
        time_start = time.time()
        proc = subprocess.Popen(
            cmd,
            # Do not use `shell=True`, which will create shell->jvm, a sub-subprocess, which
            # won't be killed just by calling shell's `.kill()`; whereas,
            # without shell, the jvm subprocess is directly returned,
            # which can be killed then.
            # shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=f'./out/pyanalyzer-{lang}')

        killed = False
        if timeout is not None:
            def handle_timeout():
                global killed
                killed = True
                proc.kill()
                logging.warning(
                    f'Running pyanalyzer-{lang} on {project_name} timed out')
                records['pyanalyzer-time'] = -1

            timer = Timer(timeout, handle_timeout)
            timer.start()

        pid = proc.pid
        memory = memory_profiling(pid)
        try:
            for line in io.TextIOWrapper(proc.stdout):
                print(line, end='')
        except UnicodeDecodeError:
            logging.warning(
                f'Suppressing an encoding error on pyanalyzer-{lang} while process {project_name}')
        time_end = time.time()

        # No matter it been killed or not, still output the peak memory usage
        records['pyanalyzer-memory'] = memory['peak']

        if not killed:
            # Cancel the timer! if the process is finished within the time
            try:
                logging.info(
                    f'pyanalyzer-{lang} finished normally, cancel the timer')
                timer.cancel()
            except:
                pass

            records['pyanalyzer-time'] = time_end - time_start

            logging.info(
                f'Running pyanalyzer-{lang} on {project_name} costs {records["pyanalyzer-time"]}s'
                + (f' and {records["pyanalyzer-memory"]}MB' if records['pyanalyzer-memory'] != -1 else ''))
    else:
        records['pyanalyzer-time'] = 0
        records['pyanalyzer-memory'] = 0


    # Run ENRE19
    if only == 'enre19' or only == '':
        print('Starting ENRE19')
        if args.lang == 'python':
            cmd = f'java -jar ./tools/ENRE19/ENRE-v2.0.jar python {abs_repo_path} null {project_name}'
        print(cmd)

        # Whether placing the start of timer here or after the creation
        # has no significant impact on the final duration
        time_start = time.time()
        proc = subprocess.Popen(
            cmd,
            # Do not use `shell=True`, which will create shell->jvm, a sub-subprocess, which
            # won't be killed just by calling shell's `.kill()`; whereas,
            # without shell, the jvm subprocess is directly returned,
            # which can be killed then.
            # shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

        killed = False
        if timeout is not None:
            def handle_timeout():
                global killed
                killed = True
                proc.kill()
                logging.warning(
                    f'Running ENRE19 on {project_name} timed out')
                records['ENRE19-time'] = -1

            timer = Timer(timeout, handle_timeout)
            timer.start()

        pid = proc.pid
        memory = memory_profiling(pid)
        try:
            for line in io.TextIOWrapper(proc.stdout):
                print(line, end='')
        except UnicodeDecodeError:
            logging.warning(
                f'Suppressing an encoding error on ENRE19 while process {project_name}')
        time_end = time.time()

        # No matter it been killed or not, still output the peak memory usage
        records['ENRE19-memory'] = memory['peak']
        if not killed:
            # Cancel the timer! if the process is finished within the time
            try:
                logging.info(
                    f'ENRE19 finished normally, cancel the timer')
                timer.cancel()
            except:
                pass

            records['ENRE19-time'] = time_end - time_start

            logging.info(
                f'Running ENRE19 on {project_name} costs {records["ENRE19-time"]}s'
                + (f' and {records["ENRE19-memory"]}MB' if records['ENRE19-memory'] != -1 else ''))
    else:
        records['ENRE19-time'] = 0
        records['ENRE19-memory'] = 0



    # Run PySonar2
    if only == 'pysonar2' or only == '':
        print('Starting PySonar2')
        if args.lang == 'python':
            project_set_path = Path(str(path.dirname(__file__)) + '\\tools\pysonar-2.1.3.jar')
            cmd = f'java -classpath {project_set_path} org.yinwang.pysonar.JSONDump {abs_repo_path} : {project_name}'
        print(cmd)

        # Whether placing the start of timer here or after the creation
        # has no significant impact on the final duration
        time_start = time.time()
        proc = subprocess.Popen(
            cmd,
            # Do not use `shell=True`, which will create shell->jvm, a sub-subprocess, which
            # won't be killed just by calling shell's `.kill()`; whereas,
            # without shell, the jvm subprocess is directly returned,
            # which can be killed then.
            # shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

        killed = False
        if timeout is not None:
            def handle_timeout():
                global killed
                killed = True
                proc.kill()
                logging.warning(
                    f'Running PySonar2 on {project_name} timed out')
                records['PySonar2-time'] = -1

            timer = Timer(timeout, handle_timeout)
            timer.start()

        pid = proc.pid
        memory = memory_profiling(pid)
        try:
            for line in io.TextIOWrapper(proc.stdout):
                print(line, end='')
        except UnicodeDecodeError:
            logging.warning(
                f'Suppressing an encoding error on PySonar2 while process {project_name}')
        time_end = time.time()

        # No matter it been killed or not, still output the peak memory usage
        records['PySonar2-memory'] = memory['peak']
        if not killed:
            # Cancel the timer! if the process is finished within the time
            try:
                logging.info(
                    f'PySonar2 finished normally, cancel the timer')
                timer.cancel()
            except:
                pass

            records['PySonar2-time'] = time_end - time_start

            logging.info(
                f'Running PySonar2 on {project_name} costs {records["PySonar2-time"]}s'
                + (f' and {records["PySonar2-memory"]}MB' if records['PySonar2-memory'] != -1 else ''))
    else:
        records['PySonar2-time'] = 0
        records['PySonar2-memory'] = 0



    # Run PyCG
    if only == 'pycg':
        print('Starting pycg')
        # abs_repo_path1 = abs_repo_path.replace("\\", "\\\\")
        path1 = str(abs_repo_path).replace("\\", "/")
        if args.lang == 'python':
            cmd = f'cd {path1} && pycg --package {project_name} $(find . -type f -name "*.py") -o {project_name}.json'
        print("cmd = " + cmd)

        # Whether placing the start of timer here or after the creation
        # has no significant impact on the final duration
        time_start = time.time()
        proc = subprocess.Popen(['D:\\git\\Git\\bin\\bash', '-c',  cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        killed = False

        if timeout is not None:
            def handle_timeout():
                global killed
                killed = True
                proc.kill()
                logging.warning(
                    f'Running PyCG on {project_name} timed out')
                records['PyCG-time'] = -1

            timer = Timer(timeout, handle_timeout)
            timer.start()


        pid = proc.pid

        memory = memory_profiling(pid)

        try:
            for line in io.TextIOWrapper(proc.stdout):
                print(line, end='')
        except UnicodeDecodeError:
            logging.warning(
                f'Suppressing an encoding error on PyCG while process {project_name}')

        time_end = time.time()
        print(killed)
        # No matter it been killed or not, still output the peak memory usage
        records['PyCG-memory'] = memory['peak']
        if not killed:
            # Cancel the timer! if the process is finished within the time
            try:
                logging.info(
                    f'PyCG finished normally, cancel the timer')
                timer.cancel()
            except:
                pass

            records['PyCG-time'] = time_end - time_start

            logging.info(
                f'Running PyCG on {project_name} costs {records["PyCG-time"]}s'
                + (f' and {records["PyCG-memory"]}MB' if records['PyCG-memory'] != -1 else ''))
        else:
            continue
    else:
        records['PyCG-time'] = 0
        records['PyCG-memory'] = 0



    if only == 'depends' or only == '':
        # Run Depends
        print('starting Depends')
        cmd = f'java -jar {path.join(path.dirname(__file__), "./tools/depends.jar")} {lang} {abs_repo_path} {project_name} -g var'

        time_start = time.time()
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd='./out/depends')

        killed = False
        if timeout is not None:
            def handle_timeout():
                global killed
                killed = True
                proc.kill()
                logging.warning(
                    f'Running Depends on {project_name} timed out')
                records['Depends-time'] = -1

            timer = Timer(timeout, handle_timeout)
            timer.start()

        pid = proc.pid
        memory = memory_profiling(pid)
        try:
            for line in io.TextIOWrapper(proc.stdout):
                print(line, end='')
        except UnicodeDecodeError:
            logging.warning(
                f'Suppressing an encoding error on Depends while process {project_name}')
        time_end = time.time()

        records['Depends-memory'] = memory['peak']
        if not killed:
            try:
                logging.info('Depends finished normally, cancel the timer')
                timer.cancel()
            except:
                pass

            records['Depends-time'] = time_end - time_start
            logging.info(
                f'Running Depends on {project_name} costs {records["Depends-time"]}s'
                + (f' and {records["Depends-memory"]}MB' if records['Depends-memory'] != -1 else ""))
    else:
        records['Depends-time'] = 0
        records['Depends-memory'] = 0

    if only == 'understand' or only == '':
        # Run Understand
        print('Starting Understand')
        upath = f'./out/understand/{project_name}.und'
        ulang = 'Python'
        cmd = f'und create -db {upath} -languages {ulang} add {abs_repo_path} analyze -all'

        time_start = time.time()
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            # `upath` has already set output path to the correct location hence there is no need to set the cwd
             cwd='./out/understand'
        )

        killed = False
        if timeout is not None:
            def handle_timeout():
                global killed
                killed = True
                proc.kill()
                logging.warning(
                    f'Running Understand on {project_name} timed out')
                records['Understand-time'] = -1

            timer = Timer(timeout, handle_timeout)
            timer.start()

        pid = proc.pid
        memory = memory_profiling(pid)
        try:
            for line in io.TextIOWrapper(proc.stdout):
                print(line, end='')
        except UnicodeDecodeError:
            logging.warning(
                f'Suppressing an encoding error on Understand while process {project_name}')
        time_end = time.time()

        records['Understand-memory'] = memory['peak']
        if not killed:
            try:
                logging.info('Process finished normally, cancel the timer')
                timer.cancel()
            except:
                pass

            records['Understand-time'] = time_end - time_start
            logging.info(
                f'Running Understand on {project_name} costs {records["Understand-time"]}s'
                + (f' and {records["Understand-memory"]}MB' if records['Understand-memory'] != -1 else ""))
    else:
        records['Understand-time'] = 0
        records['Understand-memory'] = 0

    if only == 'sourcetrail':
        # Run SourceTrail (only if the project has been created before)
        print('Start SourceTrail')
        spath = f'./out/sourcetrail/{project_name}.srctrlprj'
        if path.exists(spath):
            cmd = f'D:\\test\\sourcetrail\\Sourcetrail.exe index -f {path.join(path.dirname(__file__), spath)}'
            print(cmd)
            time_start = time.time()
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)

            killed = False
            if timeout is not None:
                def handle_timeout():
                    global killed
                    killed = True
                    proc.kill()
                    logging.warning(
                        f'Running Sourcetrail on {project_name} timed out')
                    records['SourceTrail-time'] = -1

                timer = Timer(timeout, handle_timeout)
                timer.start()

            pid = proc.pid
            memory = memory_profiling(pid)
            try:
                for line in io.TextIOWrapper(proc.stdout):
                    print(line, end='')
            except UnicodeDecodeError:
                logging.warning(
                    f'Suppressing an encoding error on SourceTrail while process {project_name}')
            time_end = time.time()

            records['SourceTrail-memory'] = memory['peak']
            if not killed:
                try:
                    logging.info('Process finished normally, cancel the timer')
                    timer.cancel()
                except:
                    pass

                records['SourceTrail-time'] = time_end - time_start
                logging.info(
                    f'Running SourceTrail on {project_name} costs {records["SourceTrail-time"]}s'
                    + (f' and {records["SourceTrail-memory"]}MB' if records['SourceTrail-memory'] != -1 else ""))
        else:
            logging.warning(
                f'No SourceTrail project for {project_name}, skipped')
            records['SourceTrail-time'] = 0
            records['SourceTrail-memory'] = 0
    else:
        records['SourceTrail-time'] = 0
        records['SourceTrail-memory'] = 0

    # Instantly save duration info whenever a project is finished analizing
    # to prevent from crashing.
    with open(f'{outfile_path}.pending', 'a+') as f:
        f.write(
            f'{project_name}'
            + f',{records["LoC"]}'
            + f',{records["Depends-time"]}'
            + f',{records["Depends-memory"]}'
            + f',{records["SourceTrail-time"]}'
            + f',{records["SourceTrail-memory"]}'
            + f',{records["Understand-time"]}'
            + f',{records["Understand-memory"]}'
            + f',{records["PySonar2-time"]}'
            + f',{records["PySonar2-memory"]}'
            + f',{records["PyCG-time"]}'
            + f',{records["PyCG-memory"]}'
            + f',{records["ENRE19-time"]}'
            + f',{records["ENRE19-memory"]}'
            + f',{records["pyanalyzer-time"]}'
            + f',{records["pyanalyzer-memory"]}'
            + '\n')

try:
    # Remove `.pending` identifier to indicates to whole process succeeded
    # After the finishing of this script, if `.pending` still exists,
    # you might want to check out log files since it's a sign of some exception
    # has taken place.
    rename(f'{outfile_path}.pending', outfile_path)
except:
    logging.error(f'Lost output file {outfile_path}!')

logging.info('Run has completed')
