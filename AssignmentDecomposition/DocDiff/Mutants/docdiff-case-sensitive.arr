# CSCI0190 (Fall 2020)

provide {overlap: overlap} end

#| 
    Does NOT illustrate the following property:

    Two words are the same if they have the same characters in the same order, regardless of case.
|#

fun overlap(doc1 :: List<String>%(is-link), doc2 :: List<String>%(is-link)) -> Number:
  doc: "Finds the overlap value of two documents."
  
 
  unique-words :: List<String> = lists.distinct(doc1 + doc2)
  
  fun make-vector(doc :: List<String>) -> List<Number>:
    doc: "Makes a vector of word frequencies for a given doc."
    
    for map(vec-word from unique-words):
      doc.filter({(doc-word): doc-word == vec-word})
         .length()
    end
  end
  
  vec1 :: List<Number> = make-vector(doc1)
  vec2 :: List<Number> = make-vector(doc2)

  
  fun dot-product(shadow vec1 :: List<Number>, shadow vec2 :: List<Number>) -> Number:
    doc: "Finds the dot product of two vectors."
    
    for fold2(sum from 0, count1 from vec1, count2 from vec2):
      sum + (count1 * count2)
    end
    #|
   where:
    dot-product([list: ], [list: ]) is 0
    dot-product([list: 2], [list: -3]) is (2 * -3)
    dot-product([list: 1, 3, 2], [list: 2, 4, 3]) is (1 * 2) + (3 * 4) + (2 * 3)
    |#
  end
  
  dot-product(vec1, vec2) / num-max(dot-product(vec1, vec1), dot-product(vec2, vec2))
  #|
where:
  doc1 = [list: "John", "likes", "to", "watch", "movies", "Mary", "likes", "to", "too"]
  doc2 = [list: "John", "also", "likes", "to", "watch", "football", "games"]
  doc3 = [list: "John", "john", "also", "likes", "to", "watch", "football", "games"]
  doc-different = [list: "nothing", "in", "common", "with", "either", "one"]
  doc-upper = map(string-toupper, doc1)

  overlap([list: "A"], [list: "a"]) is 1
  overlap(doc1, doc-upper) is 1
  overlap(doc1, doc2) is (6/13)
  overlap(doc2, doc1) is (6/13)
  overlap(doc1, doc3) is (7/13)
  overlap(doc1, doc1) is 1
  overlap(doc2, doc2) is 1
  overlap(doc1, doc-different) is 0
  overlap(doc2, doc-different) is 0
  |#
end
