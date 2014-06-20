#!/usr/bin/env /usr/bin/python


from __future__ import print_function

from random import randint
#from pprint import pprint

from patchboard import discover


pb = discover(u"http://localhost:1979/")
resources = pb.resources
users = resources.users

login = "foo-{0}".format(randint(1, 100000))
user = users.create({u'login': login})

questions = user.questions({u'category': u'Science'})
print("questions type:", type(questions))

question = questions.ask()
print("question type:", type(question))

# FIXME: this call fails
result = question.answer({u'letter': u'd'})
#print("result type:", type(result))
#print(result.correct)
#print(result.success)
