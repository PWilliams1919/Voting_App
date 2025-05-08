from PyQt6.QtWidgets import *
from gui import *
import csv

vote_dict = {}
try:
    with open('vote_results.csv', 'r') as csvfile:
        votereader = csv.reader(csvfile)
        for row in votereader:
            vote_dict[int(row[0])] = row[1]
except FileNotFoundError:
    with open('vote_results.csv','w') as newfile:
        pass
    with open('vote_results.csv', 'r') as csvfile:
        votereader = csv.reader(csvfile)
        for row in votereader:
            vote_dict[int(row[0])] = row[1]

class Logic(QMainWindow, Ui_MainWindow):

    SHOW_OTHER = False

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.buttonGroup.buttonToggled.connect(lambda: self.other_toggle(self.buttonGroup.checkedId()))

        self.clear_button.clicked.connect(lambda: self.clear_fields())

        self.save_button.clicked.connect(lambda: self.save_vote(self.voterid_textentry.text().strip(),
                                                                  self.buttonGroup.checkedId()))

        self.voterid_textentry.textChanged.connect(lambda: self.save_enable(self.buttonGroup.checkedId()))

        self.other_textentry.textChanged.connect(lambda: self.save_enable(self.buttonGroup.checkedId()))

        self.results_button.clicked.connect(lambda: self.show_chart_window(vote_dict))

        self.exit_button.clicked.connect(lambda: self.exit_function())

    def other_toggle(self, button: int) -> None:
        """
        Hides or un-hides the "Other" label and textline entry box. Is called each time the radio button selection
        is changed.
        :param button: The integer ID of the newly selected radio button.
        :return: None
        """
        if self.SHOW_OTHER and (button == -2 or button == -3):
            self.other_label.hide()
            self.other_textentry.hide()
            self.SHOW_OTHER = False
        elif not self.SHOW_OTHER and button == -4:
            self.other_label.show()
            self.other_textentry.show()
            self.SHOW_OTHER = True
        self.save_enable(button)

    def clear_fields(self) -> None:
        """
        Clears Voter ID textline entry box, "Other" textline entry box, and all radio button selections,
        resets focus on Voter ID textline and hides "Other" label/textline.
        :return: None
        """
        self.voterid_textentry.setText('')
        self.voterid_textentry.setFocus()
        self.other_textentry.setText('')
        self.buttonGroup.setExclusive(False)
        self.option1_radio.setChecked(False)
        self.option2_radio.setChecked(False)
        self.optionother_radio.setChecked(False)
        self.buttonGroup.setExclusive(True)
        self.other_toggle(-2)

    def save_enable(self, button: int) -> None:
        """
        Enables save button if voter ID is present, radio button is selected and "other" text field is filled if other
        radio button is selected. Disables save button if otherwise.
        :param button: The integer ID of the newly selected radio button.
        :return: None
        """
        if len(self.voterid_textentry.text()) > 0:
            if button == -2 or button == -3 or (button == -4 and len(self.other_textentry.text().strip()) > 0):
                self.save_button.setEnabled(True)
            else:
                self.save_button.setEnabled(False)
        else:
            self.save_button.setEnabled(False)


    def save_vote(self, voter_id: int, vote_choice: int) -> None:
        """
        If voter ID has not already been used, saves it and the candidate selection or "other" text entry to vote_dict
        :param voter_id: ID number from Voter ID textline entry box
        :param vote_choice: The integer ID of the currently selected radio button.
        :return: None
        """
        if str(voter_id).isnumeric():
            if int(voter_id) in vote_dict.keys():
                self.show_error_popup(1)
            else:
                if vote_choice == -2:
                    vote_dict[int(voter_id)] = 'Pro-Skub'
                elif vote_choice == -3:
                    vote_dict[int(voter_id)] = 'Anti-Skub'
                elif vote_choice == -4:
                    vote_dict[int(voter_id)] = str(self.other_textentry.text().strip())
        else:
            self.show_error_popup(2)
        self.clear_fields()

    def exit_function(self) -> None:
        """
        Overwrites csv file with current vote_dict values and closes program.
        :return: None
        """
        with open('vote_results.csv', 'w') as csvfile:
            vote_writer = csv.writer(csvfile, lineterminator='\n')
            for voter in vote_dict:
                vote_writer.writerow([voter, vote_dict[voter]])

        self.close()