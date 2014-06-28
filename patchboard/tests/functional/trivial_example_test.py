# trivial_example.py
#
# Copyright 2014 BitVault.
#
# Reproduces the tests in trivial_example.rb


from __future__ import print_function

import pytest
from inspect import ismethod

from patchboard import resources
from patchboard.tests.fixtures import (trivial_net_pb, trivial_net_resources,
                                       trivial_net_users, trivial_net_user,
                                       trivial_net_question)
pytest.mark.usefixtures(trivial_net_pb, trivial_net_resources,
                        trivial_net_users, trivial_net_user,
                        trivial_net_question)


def test_user_type(trivial_net_user):
    assert isinstance(trivial_net_user, resources.User)


def test_user_actions(trivial_net_user):
    assert hasattr(trivial_net_user, u'get')
    assert ismethod(trivial_net_user.get)

    assert hasattr(trivial_net_user, u'delete')
    assert ismethod(trivial_net_user.delete)


# FIXME: xfail commented out to illustrate the problem--there is a
# simple version in tests/scripts/play.py that illustrates the
# problem without using the fixtures
#@pytest.mark.xfail
def test_question_type(trivial_net_question):
    assert isinstance(trivial_net_question, resources.Question)


#@pytest.mark.xfail
def test_question_actions(trivial_net_question):
    assert hasattr(trivial_net_question, u'answer')
    assert ismethod(trivial_net_question.answer)


#@pytest.mark.xfail
def test_question_answer(trivial_net_question):
    result = trivial_net_question.answer({u'letter': u'd'})
    assert result.success
    assert result.correct == u'd'
