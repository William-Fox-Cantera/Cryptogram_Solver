"""
string_to_nums, gives each unique letter in the given sentence a unique integer
                for example: 'hello' becomes 01223. Returns it in string form 
                spaces are the letter 'x'

Consumes: sentence, a string to be converted
Produces: A string 
"""
def string_to_nums(sentence):
    chars_used = {}
    output_arr = []
    i = 0
    for letter in sentence:
        if letter.isspace():
            output_arr.append('x')
            continue
        elif letter not in chars_used: 
            chars_used[letter] = str(i)
            i += 1
        output_arr.append(chars_used[letter])
    return ''.join(map(str, output_arr))
      
"""
proces_solution, gives the output of the program if a solution is found. Also 
                 adds the solution to the current solutions list. 

Consumes: sentence, the solution
Produces: nothing
"""
def process_solution(sentence):
    print(sentence)
    current_solutions.append(sentence)
    
    
"""
is_solution, returns true if the word(s) it is given are in the dictionary
             by using binary search to search the already sorted word list,
             false otherwise.

Consumes: sentence, a word or sentence of words to check
Produces: a boolean 
"""
def is_solution(sentence, encoded_sentence):
    return string_to_nums(sentence) == string_to_nums(encoded_sentence)\
    if sentence not in current_solutions else False
 
 

"""
construct_candidates, takes in the word list and the hidden word and returns a
                      list of words valid for the next word in the sentence. 
                      
Consumes: word_list, the words from the dictionary
          sentence,  the current state of the solution
          encoded_sentence, the cryptogram
Produces: A list of words that could be in the encoded word/sentence
"""
def construct_candidates(word_list, sentence, encoded_sentence):
    candidates = []
    encoded_nums = string_to_nums(encoded_sentence)
    encoded_nums_seperate = [string_to_nums(word) for word in encoded.split(' ')] 

    for word in word_list[:]:
        add_space = ""
        offset = 1
        if len(sentence) > 0:
            add_space = " "
            offset = 0
       
        current_length = len(sentence.split(" ")) - offset
        
        # Makes sure the correct index of the word in a sentence is returned if mroe than one word has the same integer pattern
        pattern_inds = [ i for i, n in enumerate(encoded_nums_seperate) if n == string_to_nums(word) ]
        
        # Makes sure word is a candidate for the next word in the sentence    
        if current_length in pattern_inds:
           # Makes sure out of the possible matches for the next word, the entire partial solution is a valid one
            if string_to_nums(sentence + add_space + word) in string_to_nums(encoded):
                candidates.append(word)
    return candidates


"""
backtrack, the main function of this program, checks if the current candidates
           are a solution, if they are this function exits. Else it backtracks
           to try all possible solutions using an exhaustive search.
           
Consumes: word_list, dictionary of English words
          sentence, the solution being built
          encoded_sentence, the cryptogram
Produces: nothing
"""
def backtrack(word_list, sentence, encoded_sentence):
    if is_solution(sentence, encoded_sentence):
        process_solution(sentence)
    else:                       
        candidate_list = construct_candidates(word_list, sentence, encoded_sentence) 
        for word in candidate_list: 
            if sentence is "": # Case 1: Nothing in sentence yet, pick first word from candidates
                sentence += word
            else: # Case 2: sentence already has words in it 
                sentence += " " + word
            backtrack(word_list, sentence, encoded_sentence)
            if " " in sentence:
                sentence = sentence.rsplit(" ", 1)[0] 
            else:
                sentence = ""
        
     
if __name__ == '__main__':            
    words = open("dictionary.txt", "r")
    word_list = [ word.strip("\n") for word in words ]
    encoded = str(input(""))
    
    # This prunes away any invalid words. Meaning words that cannot match
    # any of the words in the hidden sentence. This only needs to be done once 
    # so its in the main.
    encoded_nums = [string_to_nums(word) for word in encoded.split(' ')] 
    for word in word_list[:]: # Must iterate over copy of the list when removing in loop
        if string_to_nums(word) not in encoded_nums:
            word_list.remove(word)
            
    # Only global variable
    current_solutions = []
    
    backtrack(word_list, "", encoded)
   
