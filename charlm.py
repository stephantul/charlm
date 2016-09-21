from collections import Counter, defaultdict
from random import random, randint

class CharLm:

    def __init__(self, filename, order, paddingchar="~"):
        """
        A character Language model of order n.
        Based on code by Yoav Goldberg: https://gist.github.com/yoavg/d76121dfde2618422139

        :param filename: The file from which to read text.
        :param order: The order of the character model.
        :return: None
        """

        self.file = filename
        self.order = order

        padding = paddingchar * order
        lm = defaultdict(Counter)

        for idx, line in enumerate(open(filename)):

            line = line.strip().replace(paddingchar, "-")

            if not line:
                continue

            line = padding + line + padding

            for i in range(len(line)-order):
                history, char = line[i:i+order], line[i+order]
                lm[history][char] += 1

        self.lm = {k: self.normalize(v) for k, v in lm.items()}

    @staticmethod
    def normalize(dictionary):
        """
        Helper function to normalize the counts to probabilities.

        :param dictionary: A dictionary with a history as keys, and dictionaries of character counts as values.
        :return: The normalized dictionary
        """

        s = sum(dictionary.values())
        return [(c, cnt/s) for c, cnt in dictionary.items()]

    def generate_letter(self, history):
        """
        Generate a single letter from some history.

        :param history: A string representing the currently generated text.
        :return: a character.
        """

        distribution = self.lm[history[-self.order:]]

        # generate a random number between 0 and 1.
        x = random()
        for char, probability in distribution:

            # subtract the probability of the current character from the random number.
            x = x - probability
            # If the random number is below 0, return the current character.
            if x <= 0:
                return char

    def generate(self, nletters=1000):
        """
        Generate n letters, based on a starting symbol and the language model.
        The model generates successive letters based on calls to "generate_letter", above.

        :param nletters: the number of letters to generate
        :return: a text.
        """

        # have to start with some history.
        history = "~" * self.order
        out = []
        for i in range(nletters):
            c = self.generate_letter(history)
            history = history[-self.order:] + c
            out.append(c)
        return "".join(out).replace("~" * self.order, "\n")


if __name__ == "__main__":

    model = CharLm("charles.txt", 15)
    print("done")
