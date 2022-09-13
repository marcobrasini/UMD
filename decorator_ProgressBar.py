"""

"""


import sys
import math
import functools as ft


class ProgressBar:
    """
    Class decorator to display the progress bar of a iterative process.

    The object can decorate iterative functions yelding an iterator.
    """

    def __init__(self, length, stream=sys.stdout, msg=''):
        """
        Construct the progress bar decorator.

        Parameters
        ----------
        length : int
            The length of the bar.
        stream : output stream, optional
            The output stream where to display the progress bar.
            The default is sys.stdout.
        msg : string, optional
            A message string to display before the progress bar.
            The default is ''.

        Returns
        -------
        ProgressBars decorator.

        """
        self.barMsg = str(msg)
        self.barLength = int(length)
        self.barStream = stream
        self.barStep = 1/self.barLength
        self.barLoaded = 0

    def __call__(self, func):
        """
        Overload of the __call__ function.

        Parameters
        ----------
        func : function
            The function to decorate.
        *args : arg list
            List of the function arguments.
        **kwargs : kwarg
            List of the function key-word arguments.

        Returns
        -------
        TYPE
            The result of the function func(*args, **kwargs).

        """
        @ft.wraps(func)
        def wrapper(*args, **kwargs):
            # Print the initial empty bar.
            self.printbeg()
            # Define the iterator through the function yielding
            progress_generator = func(*args, **kwargs)
            try:
                while True:
                    # Execute the iterator in the function.
                    # If a good value is yield, it updates the progress bar.
                    progress = next(progress_generator)
                    if progress >= 0 and progress < 1:
                        self.update(progress)
                    else:
                        error_msg = "wrapped function must yield 0 <= i < 1."
                        raise(ValueError(error_msg))
            # If the StopIteration is yield, print the completly full bar.
            except StopIteration as result:
                self.printend()
                return result
        return wrapper

    def update(self, progress):
        """
        Update the progress bar value and print the new progress bar.

        Parameters
        ----------
        progress : float
            The percentage of the progress.

        Returns
        -------
        None.

        """
        if progress > self.barLoaded*self.barStep:
            self.barLoaded = math.ceil(progress/self.barStep)
            self.printbar(progress)

    def printbeg(self):
        """
        Print the initially completly empty progress bar.

        Returns
        -------
        None.

        """
        todo = " "*int(self.barLength)
        bar = "["+todo+"] {:5.1f}%".format(0)
        self.barStream.write('\r'+self.barMsg+' '+bar)
        self.barStream.flush()

    def printbar(self, perc):
        """
        Print the updated progress bar.

        Parameters
        ----------
        perc : float
            The percentage of the progress.

        Returns
        -------
        None.

        """
        done = "="*self.barLoaded
        toto = " "*(self.barLength - self.barLoaded)
        bar = "["+done+toto+"] {:5.1f}%".format(perc*100)
        self.barStream.write('\r'+self.barMsg+' '+bar)
        self.barStream.flush()

    def printend(self):
        """
        Print the finally completly full progress bar.

        Returns
        -------
        None.

        """
        done = "="*int(self.barLength)
        bar = "["+done+"] {:5.1f}%\n".format(100)
        self.barStream.write('\r'+self.barMsg+' '+bar)
        self.barStream.flush()
