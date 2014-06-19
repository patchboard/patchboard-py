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

# FIXME:
# Problem 1 (probably the root problem): user.questions() only  takes
# 1 argument (in Python self counts, so it's a zero-argument method by most
# people's count).
questions = user.questions({u'category': u'Science'})
# It's a pain to track down calls to dynamically created methods, but
# the function being called seems to be the one constructed at
# resource.py:37. I suspect it's not the correct function getting called,
# since this all works in the ruby client.

## This works, but it's kind of pointless to look at what it does
## if it isn't the right call in the first place.
#questions = user.questions()  # ({u'category': u'Science'})
## Doing this, you get back a dict instead of a Questions object, but
## I suspect this is simply a symptom of the above problem
#print("Questions:", questions)
#print("Questions type:", type(questions))
