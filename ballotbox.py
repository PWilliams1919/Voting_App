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

    def get_vote_dict(self) -> dict:
        """
        Returns current vote_dict attribute of the object.
        :return: vote_dict dictionary
        """
        return self.__vote_dict

    def check_id(self, voter_id: str) -> bool:
        """
        Checks if entered voter ID number has already been used.
        :param voter_id: Entered voter ID
        :return: status on if that ID can cast a vote
        """
        if int(voter_id) in self.__vote_dict.keys():
            return False
        else:
            return True

    def add_vote(self, voter_id: str, candidate: str) -> None:
        """
        Adds voter ID and vote to objects vote dictionary.
        :param voter_id: Entered voter ID
        :param candidate: Selected candidate
        """
        self.__vote_dict[voter_id] = candidate