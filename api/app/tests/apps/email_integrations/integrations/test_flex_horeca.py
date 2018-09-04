from unittest import mock

from django.conf import settings
from django.test import TestCase
from freezegun import freeze_time

from signals.apps.signals import tasks
from tests.apps.signals.factories import SignalFactory


class TestTaskSendMailFlexHoreca(TestCase):

    @mock.patch('signals.apps.signals.tasks.send_mail')
    @mock.patch('signals.apps.signals.tasks.loader')
    @mock.patch('signals.apps.signals.tasks.'
                '_is_signal_applicable_for_flex_horeca',
                return_value=True)
    def test_send_mail_flex_horeca(
            self,
            mocked_is_signal_applicable_for_flex_horeca,
            mocked_loader,
            mocked_send_mail):
        # Setting up template mocking.
        mocked_rendered_template = mock.Mock()
        mocked_template = mock.Mock()
        mocked_template.render.return_value = mocked_rendered_template
        mocked_loader.get_template.return_value = mocked_template

        # Creating a `Signal` object to use for sending mail to Flex Horeca.
        signal = SignalFactory.create()
        tasks.send_mail_flex_horeca(pk=signal.id)

        # Asserting all correct function calls.
        mocked_loader.get_template.assert_called_once_with(
            'mail_flex_horeca.txt')
        mocked_template.render.assert_called_once_with({'signal': signal})

        mocked_is_signal_applicable_for_flex_horeca.assert_called_once_with(
            signal)
        mocked_send_mail.assert_called_once_with(
            subject='Nieuwe melding op meldingen.amsterdam.nl',
            message=mocked_rendered_template,
            from_email=settings.NOREPLY,
            recipient_list=(settings.EMAIL_APPTIMIZE_INTEGRATION_ADDRESS, ),
            fail_silently=False)

    @mock.patch('signals.apps.signals.tasks.send_mail')
    @mock.patch('signals.apps.signals.tasks.log')
    def test_send_mail_flex_horeca_no_signal_found(
            self, mocked_log, mocked_send_mail):
        tasks.send_mail_flex_horeca(pk=1)  # id `1` shouldn't be found.

        mocked_log.exception.assert_called_once()
        mocked_send_mail.assert_not_called()

    @mock.patch('signals.apps.signals.tasks.send_mail')
    @mock.patch('signals.apps.signals.tasks.'
                '_is_signal_applicable_for_flex_horeca',
                return_value=False)
    def test_send_mail_flex_horeca_not_applicable(
            self,
            mocked_is_signal_applicable_for_flex_horeca,
            mocked_send_mail):
        signal = SignalFactory.create()

        tasks.send_mail_flex_horeca(pk=signal.id)

        mocked_is_signal_applicable_for_flex_horeca.assert_called_once_with(
            signal)
        mocked_send_mail.assert_not_called()


class TestHelperIsSignalApplicableForFlexHoreca(TestCase):

    @freeze_time('2018-08-03')  # Friday
    def test_is_signal_applicable_for_flex_horeca_in_category_on_friday(self):
        signal = SignalFactory.create(
            category__main='Overlast Bedrijven en Horeca',
            category__sub='Geluidsoverlast muziek')

        result = tasks._is_signal_applicable_for_flex_horeca(signal)

        self.assertEqual(result, True)

    @freeze_time('2018-08-04')  # Saterday
    def test_is_signal_applicable_for_flex_horeca_in_category_on_saterday(
            self):
        signal = SignalFactory.create(
            category__main='Overlast Bedrijven en Horeca',
            category__sub='Geluidsoverlast muziek')

        result = tasks._is_signal_applicable_for_flex_horeca(signal)

        self.assertEqual(result, True)

    @freeze_time('2018-08-03')  # Friday
    def test_is_signal_applicable_for_flex_horeca_outside_category_on_friday(
            self):
        signal = SignalFactory.create(
            category__main='Some other main category',
            category__sub='Some other sub category')

        result = tasks._is_signal_applicable_for_flex_horeca(signal)

        self.assertEqual(result, False)

    @freeze_time('2018-08-05')  # Sunday
    def test_is_signal_applicable_for_flex_horeca_in_category_on_sunday(
            self):
        signal = SignalFactory.create(
            category__main='Overlast Bedrijven en Horeca',
            category__sub='Geluidsoverlast muziek')

        result = tasks._is_signal_applicable_for_flex_horeca(signal)

        self.assertEqual(result, False)
