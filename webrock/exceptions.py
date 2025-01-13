class WebrockBaseError(Exception):
    """
    The base error for all webrock errors
    """


class AgentExectorFatalError(WebrockBaseError):
    """
    An error for gpt to throw when it's not sure how to complete the task or somethings else unexpected happens
    """


class MaxSequencesExceededError(WebrockBaseError):
    """
    An error thrown when the maximum number of sequences has been reached without completing
    """
