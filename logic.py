from PyQt6.QtWidgets import *
from gui import *
from ballotbox import *

class Logic(QMainWindow, Ui_MainWindow):

    SHOW_OTHER = False

    ballotbox = Ballotbox()

    def __init__(self):
        """
        Initializes program window
        """
        super().__init__()
        self.setupUi(self)

        self.buttonGroup.buttonToggled.connect(lambda: self.other_toggle(self.buttonGroup.checkedId()))

        self.clear_button.clicked.connect(lambda: self.clear_fields())

        self.save_button.clicked.connect(lambda: self.save_vote(self.voterid_textentry.text().strip(),
                                                                  self.buttonGroup.checkedId()))

        self.voterid_textentry.textChanged.connect(lambda: self.save_enable(self.buttonGroup.checkedId()))

        self.other_textentry.textChanged.connect(lambda: self.save_enable(self.buttonGroup.checkedId()))

        self.results_button.clicked.connect(lambda: self.show_chart_window(self.ballotbox.get_vote_dict()))

        self.exit_button.clicked.connect(lambda: self.exit_function())

    def other_toggle(self, button: int) -> None:
        """
        Hides or un-hides the "other" label and textline entry box. Is called each time the radio button selection
        is changed.
        :param button: The integer ID of the newly selected radio button.
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
        Clears Voter ID textline entry box, "other" textline entry box, and all radio button selections,
        resets focus on Voter ID textline and hides "other" label/textline.
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
        Enables save button if voter ID is present and a radio button is selected (requires "other" text
        field is filled if "other" radio button is selected). Disables save button if requirements aren't met.
        :param button: The integer ID of the newly selected radio button.
        """
        if len(self.voterid_textentry.text()) > 0:
            if button == -2 or button == -3 or (button == -4 and len(self.other_textentry.text().strip()) > 0):
                self.save_button.setEnabled(True)
            else:
                self.save_button.setEnabled(False)
        else:
            self.save_button.setEnabled(False)


    def save_vote(self, voter_id: int, vote_index: int) -> None:
        """
        Validates voter ID is integer and checks for previous use, if valid sends voter ID and vote to Ballotbox object.
        :param voter_id: ID number from Voter ID textline entry box
        :param vote_index: The integer ID of the currently selected radio button.
        """
        if str(voter_id).isnumeric():
            choice = ''
            can_vote = self.ballotbox.check_id(str(voter_id))
            print(can_vote)
            if can_vote:
                if vote_index == -2:
                    choice = 'Pro-Skub'
                elif vote_index == -3:
                    choice = 'Anti-Skub'
                elif vote_index == -4:
                    choice = str(self.other_textentry.text().strip())

                self.ballotbox.add_vote(voter_id, choice)
            else:
                self.show_error_popup(1)
        else:
            self.show_error_popup(2)
        self.clear_fields()

    def exit_function(self) -> None:
        """
        Overwrites existing csv file with current Ballotbox contents and closes program.
        """
        with open('vote_results.csv', 'w') as csvfile:
            write_dict = self.ballotbox.get_vote_dict()
            vote_writer = csv.writer(csvfile, lineterminator='\n')
            for voter in write_dict:
                vote_writer.writerow([voter, write_dict[voter]])

        self.close()