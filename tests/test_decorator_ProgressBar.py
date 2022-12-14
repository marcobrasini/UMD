"""
===============================================================================
                                ProgressBar tests
===============================================================================
"""


from ..utils.decorator_ProgressBar import ProgressBar

import sys
import unittest.mock as mock
import pytest
import hypothesis as hp
import hypothesis.strategies as st


class TestProgressBar_object:
    """
    Test a ProgressBar obeject of length 10, with barStep of 0.1.

    """

    msg = 'testBar'
    length = 10
    stream = sys.stdout

    bar = ProgressBar(length=length, stream=stream, msg=msg)

    def test_ProgressBar_init(self):
        """
        Test the __init__ function assignement operations.

        """
        self.bar.barMsg == self.msg
        self.bar.barLength == self.length
        self.bar.barStream == self.stream
        self.bar.barStep == 1/self.length
        self.bar.barLoaded == 0

    @mock.patch.object(stream, 'flush')
    @mock.patch.object(stream, 'write')
    def test_ProgressBar_printbeg(self, mock_write, mock_flush):
        """
        Test the printbeg function. Assert the call of the write method with an
        empty progress bar and the call of the flush methods.

        """
        self.bar.printbeg()
        emptybar = '\r'+self.msg+' [          ]   0.0%'
        mock_write.assert_called_once_with(emptybar)
        mock_flush.assert_called_once()

    @mock.patch.object(stream, 'flush')
    @mock.patch.object(stream, 'write')
    def test_ProgressBar_printend(self, mock_write, mock_flush):
        """
        Test the printend function. Assert the call of the write method with a
        full progress bar and the call of the flush methods.

        """
        self.bar.printend()
        fullbar = '\r'+self.msg+' [==========] 100.0%\n'
        mock_write.assert_called_once_with(fullbar)
        mock_flush.assert_called_once()

    @mock.patch.object(stream, 'flush')
    @mock.patch.object(stream, 'write')
    def test_ProgressBar_printbar(self, mock_write, mock_flush):
        """
        Test the printbar function. For a barLoaded parameter equal to 3/10
        and a progress of 0.25, it asserts the call of the write method with
        the progress bar and the call of the flush methods.

        """
        progress = 0.25
        self.bar.barLoaded = 3
        self.bar.printbar(progress)
        tempbar = '\r'+self.msg+' [===       ] {:5.1f}%'.format(100*progress)
        mock_write.assert_called_once_with(tempbar)
        mock_flush.assert_called_once()

    @mock.patch.object(ProgressBar, 'printbar')
    def test_ProgressBar_update_new(self, mock):
        """
        Test the update function. For a barLoaded parameter equal to 2/10 and
        a progress of 0.25, it updates the barLoaded parameter and call the
        printbar method with the same progress value.

        """
        progress = 0.25
        self.bar.barLoaded = 2
        self.bar.update(progress)
        mock.assert_called_once_with(progress)
        assert self.bar.barLoaded == 3

    @mock.patch.object(ProgressBar, 'printbar')
    def test_ProgressBar_update_old(self, mock):
        """
        Test the update function. For a barLoaded parameter equal to 3/10 and
        a progress of 0.25, it does not updates the barLoaded parameter and
        does not call the printbar method.

        """
        progress = 0.25
        self.bar.barLoaded = 3
        self.bar.update(progress)
        mock.assert_not_called()
        assert self.bar.barLoaded == 3

    @mock.patch.object(ProgressBar, 'printbar')
    def test_ProgressBar_update_far(self, mock):
        """
        Test the update function. For a barLoaded parameter equal to 3/10 and
        a progress of 0.55, it updates the barLoaded parameter to 6/10 and call
        the printbar method.

        """
        progress = 0.55
        self.bar.barLoaded = 3
        self.bar.update(progress)
        mock.assert_called_once_with(progress)
        assert self.bar.barLoaded == 6


class TestProgressBar_wrap:
    """
    Test a ProgressBar object of length 10 and of barStep 0.1, decorating a
    trivial function yielding its progress state.

    """

    length = 10
    stream = sys.stdout
    msg = 'testBar'

    @ProgressBar(length=length, stream=stream, msg=msg)
    def yielding(self, n):
        """
        Trial function yielding its progress state over the n iterations.

        """
        for i in range(n):
            yield float(i/n)

    @mock.patch.object(ProgressBar, 'update')
    def test_ProgressBar_update_call_count(self, mock):
        """
        Test the number of times the update method is called. The total number
        of calls must be equal to the total number of the function yields, n.

        """
        self.yielding(1044)
        assert mock.call_count == 1044

    @mock.patch.object(ProgressBar, 'printbar')
    @hp.given(niter=st.integers(0, 10000))
    def test_ProgressBar_printbar_call_count(self, niter, mock):
        """
        Test the number of times the printbar method is called. The total
        number of calls must be equal to the length of the progress bar.

        """
        self.yielding(niter)
        if niter < 2:
            assert mock.call_count == 0
        else:
            assert mock.call_count == min(niter-1, self.length)
        mock.reset_mock()

    @mock.patch.object(ProgressBar, 'printbeg')
    @hp.given(niter=st.integers(0, 10000))
    def test_ProgressBar_printbeg_call_count(self, niter, mock):
        """
        Test the number of times the printbeg method is called. It must be
        called just once at the beginning of the function.

        """
        self.yielding(niter)
        mock.assert_called_once()
        mock.reset_mock()

    @mock.patch.object(ProgressBar, 'printend')
    @hp.given(niter=st.integers(0, 10000))
    def test_ProgressBar_printend_call_count(self, niter, mock):
        """
        Test the number of times the printend method is called. It must be
        called just once at the end of the function.

        """
        self.yielding(niter)
        mock.assert_called_once()
        mock.reset_mock()

    @hp.given(yielded=st.floats(max_value=0, exclude_max=True))
    def test_ProgressBar_progress_error_negative(self, yielded):
        """
        Test the function decoration for an uncorrect progress value yielded.
        If the progress value is negative an AttributeError is raised.

        """
        @ProgressBar(length=self.length, stream=self.stream, msg=self.msg)
        def yielding_error_negative(n):
            yield yielded
        with pytest.raises(ValueError):
            yielding_error_negative(1044)

    @hp.given(yielded=st.floats(min_value=1, exclude_min=True))
    def test_ProgressBar_progress_error_too_large(self, yielded):
        """
        Test the function decoration for an uncorrect progress value yielded.
        If the progress value is larger or equal to 1.0 an AttributeError is
        raised.

        """
        @ProgressBar(length=self.length, stream=self.stream, msg=self.msg)
        def yielding_error_too_large(n):
            yield yielded
        with pytest.raises(ValueError):
            yielding_error_too_large(1044)
