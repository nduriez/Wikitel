
from Teletel import Teletel
from views.ViewController import *


class ListViewController(ViewController):

    def __init__(self, baudrate, port, list_title, list_to_display=None):
        super().__init__(baudrate, port)

        self.top_of_page = ()  # x,y position of top of page

        self.list_title = list_title
        self.displayed_list = []
        if list_to_display:
            self.displayed_list = list_to_display  # current displayed list
            self.displayed_list = ["test", "salut", "coucou", "\n bonjou\nr", "\n", "a"]

    def draw(self):
        super().draw()
        #
        # self._minitel.inverse(True)
        # self._minitel._print("Résultats de recherche pour:")
        # self._minitel.inverse(False)
        self._minitel._print(self.list_title + "\n")
        self._minitel.plot("_", 40)

        self.top_of_page = self._minitel.curpos()

        if self.displayed_list:
            self.print_list()

    def print_list(self, list_to_print=None):
        """
        Print a numerated list

        :param list[str] list_to_print: List of element to print
        """
        if list_to_print:
            self.displayed_list = list_to_print

        for i, elem in enumerate(self.displayed_list):
            self._print_line(i+1, elem)

        self._minitel.pos(self._minitel.LINE_SIZE,
                          self._minitel.COL_SIZE - 1)  # pos cursor at bottom right because of local echo

    def _print_line(self, index, text, reverse=False):
        elem_index = "{})".format(index)

        self._minitel.inverse(not reverse)
        self._minitel._print(elem_index)
        self._minitel.inverse(reverse)

        self._minitel._print(text)
        curPos = self._minitel.curpos()
        self._minitel._del(*curPos)
        self._minitel._print("\n")

    def handle_input(self):
        """
        Handle the selection of an item on the list by the user

        :return: the selected item
        :rtype: str
        """
        selected_elem = self.displayed_list[0]
        i = 1
        do_error_happened = False
        while True:
            data = self._minitel.input(self._minitel.LINE_SIZE, self._minitel.COL_SIZE-2, 2)

            try:
                if data[0] == '' and data[1] == Teletel.ENVOI.value:
                    return selected_elem

                if not do_error_happened:
                    previous_i = i
                do_error_happened = False
                i = int(data[0])
                if 0 > i-1 or i-1 > len(self.displayed_list):   # Check out of bounds
                    raise IndexError

                # Redraw previously selected element
                padding = sum([self.calculate_nb_of_lines(self.displayed_list[previouss_i - 1]) for previouss_i in range(previous_i)])
                self._minitel.pos(self.top_of_page[0] - 1 + padding)
                self._print_line(previous_i, selected_elem, False)

                selected_elem = self.displayed_list[i - 1]

                # Draw current selected element with emphasis
                padding = sum([self.calculate_nb_of_lines(self.displayed_list[previouss_i - 1]) for previouss_i in range(i)])
                self._minitel.pos(self.top_of_page[0] - 1 + padding)
                self._print_line(i, selected_elem, True)

                self._minitel.pos(self._minitel.LINE_SIZE, self._minitel.COL_SIZE-1)    # pos cursor at bottom right because of local echo

            except ValueError:
                self._minitel.message(0, 1, 1, "ERREUR: Utilisez le pavé numérique", True)
                do_error_happened = True
            except IndexError:
                self._minitel.message(0, 1, 1, "ERREUR: Index invalide.", True)
                do_error_happened = True

    def _draw_footer(self):
        pass
