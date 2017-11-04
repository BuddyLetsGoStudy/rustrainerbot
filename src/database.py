# coding: utf-8


class States:
    """
        Static class with the states of the our FSM (final-state machines)
    """
    IDLE = 0
    WAIT = 1

    @staticmethod
    def state(state):
        """
        A little helper for debugging
        
        :param state: <int>
        :return: state label <str>
        """
        return filter(lambda x: getattr(States, x) == state, vars(States)).__next__()


class User(object):
    MIN_TELEGRAM_ID = 10 ** 8

    def __init__(self, tg_id: int, state, amount: int=0):
        """
        
        :param tg_id: telegram user id <int>
        :param state: initial state <States: state>
        :param amount: initial amount of the words <int>
        """
        self.id = tg_id
        self.state = state
        self.amount = amount
        self.word = None

        if tg_id < self.MIN_TELEGRAM_ID:
            raise BadTelegramIdError("id = %d is lower than the minimal allowed telegram id: %d" %
                                     (tg_id, self.MIN_TELEGRAM_ID))

    def __repr__(self):
        return "User(tg_id={0}, state={1}, amount={2})".format(self.id, self.state, self.amount)


class Users(object):

    def __init__(self):
        """
        A database class. 
        Supports simple transactions.
        """

        # main table of the database
        self.users = dict()

    def add(self, tg_id, state=States.IDLE, amount=0):
        """
        Adds user to the table.
        
        :param tg_id: telegram user id <int>
        :param state: state <States: state>
        :param amount: amount of words <int>
        :return: result of the transaction <bool>
        """

        # if user is already exists abort the transaction
        if tg_id in self.users:
            return False

        user = User(tg_id, state, amount)
        self.users[user.id] = user

        return True

    def change_column(self, tg_id, column, value):
        """
        A simple transaction method.
        
        :param tg_id: telegram user id <int>
        :param column: column name <str>
        :param value: value to insert <any>
        :return: pointer to self
        """

        # if user is unknown raise an exception
        if tg_id not in self.users:
            raise UnknownUserException("User with id = %d does not exist." % tg_id)

        # if bad column is provided raise an exception
        if not hasattr(self.users[tg_id], column):
            raise UnknownColumnException("User object does not have a %s column" % column)

        setattr(self.users[tg_id], column, value)
        return self

    def __getitem__(self, tg_id):
        """
        [] operator overloading
        
        :param tg_id: telegram user id <int>
        :return: user object <User>
        """

        # if user is unknown raise an exception
        if tg_id not in self.users:
            raise UnknownUserException("User with id = %d does not exist." % staticmethod)

        return self.users[tg_id]

    def __setitem__(self, tg_id, state):
        """
        [] operator overloading
        
        :param tg_id: telegram user id <int>
        :param state: new statement <States: state>
        :return: updated user object <User>
        """

        self.change_column(tg_id, 'state', state)
        return self.users[tg_id]

    def __contains__(self, tg_id):
        """
        `in` operator overloading
        
        :param tg_id: telegram user id <int>
        :return: is user in the table <bool>
        """
        return tg_id in self.users

    def __repr__(self):
        return repr(self.users)


class UnknownUserException(ValueError):
    pass


class UnknownColumnException(ValueError):
    pass


class BadTelegramIdError(ValueError):
    pass
