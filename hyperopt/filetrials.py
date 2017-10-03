"""
File-based Trials Object
===========================

Components involved:

- filesystem

"""

import pickle

from .base import Trials

class FileTrials(Trials):
    def __init__(self, exp_key=None, refresh=True, persisted_location=None):
        super(FileTrials, self).__init__(exp_key=exp_key, refresh=refresh)

        if persisted_location is not None:
            self._persisted_file = open(persisted_location, 'a+b')

            try:
                self._persisted_file.seek(0)
                docs = pickle.load(self._persisted_file)
                super(FileTrials, self)._insert_trial_docs(docs)
                self.refresh()
            except EOFError:
                None

    def _insert_trial_docs(self, docs):
        rval = super(FileTrials, self)._insert_trial_docs(docs)

        self._persisted_file.seek(0)
        self._persisted_file.truncate()
        pickle.dump(self._dynamic_trials, self._persisted_file)
        self._persisted_file.flush()

        return rval

