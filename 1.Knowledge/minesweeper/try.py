def main():
    sentence = [1, 2, 3, 4, 5, 6, 7, 8]

    for num1 in sentence:
        for num2 in sentence:

            if num1 is num2:
                continue
            print(num1, num2)

















    """
        # checking if the number of cells is equal to counter
        if len(main_sentence.cells) == main_sentence.count:
            for cell in main_sentence.cells:
                self.mark_mine(cell)
        
        if len(main_sentence.cells) == 0:
            return
        
        if len(self.knowledge) == 0:
            self.knowledge.append(main_sentence.cells)
            return

        for sentence in self.knowledge: # sentences that already inside of knowledge
 
            # checks if the sentence is empty; if it is, loop continues
            if len(sentence) == 0:
                continue

            # checks if cell is a mine or safe if and only if sentence contains just a cell and a count
            if len(sentence) == 1 and type(sentence.count) == int:
                # if count is zero, then cell is safe
                if sentence.count == 0:
                    self.mark_safe(sentence.cells)
                elif sentence.count == 1:
                    self.mark_mine(sentence.cells)
                else:
                    print(f"there is something wrong with = {sentence.cells}")

            if len(sentence.cells) > len(main_sentence.cells):
                print("set= sentece | subset= main ")
                # checks if the main_sentence is a subset of sentence
                if self.check_subset(main_sentence, sentence):
                    # if the main sentence is a subset of sentence
                    # removes the common cells and updates the count value
                    for cell in main_sentence.cells:
                        sentence.remove(cell)
                    sentence.count -= main_sentence.count

            if len(sentence.cells) < len(main_sentence.cells):
                print("set= main | subset= sentence ")
                # checks if the sentence is a subset of main_sentence
                if self.check_subset(sentence, main_sentence):
                    # if the sentence is a subset of main_sentence
                    # removes the common cells and updates the count value
                    for cell in sentence.cells:
                        main_sentence.cells.remove(cell)
                    main_sentence.count -= sentence.count
            
            if len(sentence.cells) == len(main_sentence.cells):
                print("set= both | subset= both ")
                # checks the sentences are subsets of each other since their lenght is the same
                if self.check_subset(sentence, main_sentence):
                    # if the sentence is a subset of main_sentence
                    # removes the common cells and updates the count value
                    for cell in sentence:
                        main_sentence.cells.remove(cell)
                    sentence.count -= sentence.count

            # removes empty sentence
            if len(sentence.cells) == 0 and sentence.count == 0:
                self.knowledge.remove(sentence)
                return

            # checks that modified sentence is a mine sentence (len(sentence) == sentence_count)
            if len(sentence.cells) == sentence.count:
                for cell in sentence:
                    self.mines.add(cell)
                self.mark_mine(sentence)

            # checks that modified sentence is a safe sentence (sentence_count == 0)
            if len(sentence.cells) == 0:
                for cell in sentence:
                    self.safes.add(cell)
                self.mark_safe(sentence)
            
            self.knowledge.append(sentence)
    """


if __name__ == "__main__":
    main()
