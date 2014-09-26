# -*- coding: utf-8 -*-
#!/usr/bin/env /usr/bin/python

from __future__ import print_function

import subprocess
import tarfile, os

from glob import glob
from time import sleep
from urllib import urlretrieve
from random import randint
from patchboard import discover


# This repo contains a coffeescript patchboard server.
try:
    example_dir = glob("automatthew*")
    if not example_dir:
        if not os.path.exists(u'./pb-ex.tar.gz'):
            retrieving
            urlretrieve(u'http://github.com/automatthew/patchboard-examples/tarball/master',
                        u'./pb-ex.tar.gz')
        with tarfile.open(u'./pb-ex.tar.gz', u'r:gz') as tar:
            for tarmember in tar.getnames():
                if u'trivial' in tarmember:
                    trivial_dir = trivial_dir if u'trivial_dir' in locals() else tarmember
                    tar.extract(tarmember)
    else:
        trivial_dir = "{}/{}/".format(example_dir[0], u'trivial')

    trivial_dir = os.getcwd() + '/' + trivial_dir

    subprocess.Popen(u'npm install', cwd=trivial_dir, shell=True).wait()
    server = subprocess.Popen(u'bin/server.coffee test/data/questions.json', cwd=trivial_dir, shell=True)

    # Uuuuugh, need a better way to delay until the server is listening that doesn't wait for the process to terminate.
    sleep(2)

    pb = discover(u'http://localhost:1979/')
    resources = pb.resources
    users = resources.users

    login = "foo-{0}".format(randint(1, 100000))
    user = users.create({u'login': login})

    questions = user.questions({u'category': u'Science'})
    print("questions type:", type(questions))

    question = questions.ask()
    print("question type:", type(question))

    result = question.answer({u'letter': u'd'})

    # TODO Need to terminate this process after the test suite runs, or we'll get a port error.
    # server.terminate()

except Exception as e:
    if server:
        server.kill()
    print(e)
    SystemExit(1)
