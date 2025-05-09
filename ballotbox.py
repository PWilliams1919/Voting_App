import csv

class Ballotbox:
    def __init__(self) -> None :
        """
        Initializes a Ballotbox object.
        """
        self.__vote_dict: dict = {}

        try:
            with open('vote_results.csv', 'r') as csvfile:
                votereader = csv.reader(csvfile)
                for row in votereader:
                    self.__vote_dict[int(row[0])] = row[1]
        except FileNotFoundError:
            with open('vote_results.csv', 'w') as newfile:
                pass
            with open('vote_results.csv', 'r') as csvfile:
                votereader = csv.reader(csvfile)
                for row in votereader:
                    self.__vote_dict[int(row[0])] = row[1]

    def get_vote_dict(self):
        return self.__vote_dict

    def check_id(self, voter_id):
        can_vote = False
        if voter_id in self.__vote_dict:
            can_vote = False
        else:
            can_vote = True

        return can_vote

    def add_vote(self, voter_id, candidate):
        self.__vote_dict[voter_id] = candidate