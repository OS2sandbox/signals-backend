from unittest import mock

from django.test import TestCase

from signals.apps.signals.models import create_initial
from tests.apps.signals.factories import SignalFactory


class TestSignalReceivers(TestCase):

    @mock.patch('signals.apps.sigmax.signal_receivers.tasks', autospec=True)
    def test_create_initial_handler(self, mocked_tasks):
        signal = SignalFactory.create()
#         create_initial.send(sender=self.__class__, signal_obj=signal)

#         mocked_tasks.push_to_sigmax.delay.assert_called_once_with(pk=signal.id)

        # create signal, update it to VERZENDEN status, check that mocked task is called
