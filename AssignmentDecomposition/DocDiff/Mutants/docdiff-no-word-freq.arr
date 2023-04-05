# CSCI0190 (Fall 2020)

provide {overlap: overlap} end

#| wheat (tdelvecc, Aug 26, 2020): 
    

    DOES NOT OBEY THIS SUBPROPERTY

     The indices of the vector correspond to words that are found in either document. The value at each index is how many times the corresponding word occurs in the document.

     This basically sets frequency to 1/0.
|#

fun overlap(doc1 :: List<String>%(is-link), doc2 :: List<String>%(is-link)) -> Number:
  doc: "Finds the overlap value of two documents."
  
  doc1-lower :: List<String> = doc1.map(string-to-lower)
  doc2-lower :: List<String> = doc2.map(string-to-lower)
  
  unique-words :: List<String> = lists.distinct(doc1-lower + doc2-lower)
  
  fun make-vector(doc :: List<String>) -> List<Number>:
    doc: "Makes a vector of words for a given doc."
    

    # Change this
    for map(vec-word from unique-words):
      if doc.member(vec-word):
        1
      else:
        0
      end
    end
  end
  
  vec1 :: List<Number> = make-vector(doc1-lower)
  vec2 :: List<Number> = make-vector(doc2-lower)

  
  fun dot-product(shadow vec1 :: List<Number>, shadow vec2 :: List<Number>) -> Number:
    doc: "Finds the dot product of two vectors."
    
    for fold2(sum from 0, count1 from vec1, count2 from vec2):
      sum + (count1 * count2)
    end
  end
  
  dot-product(vec1, vec2) / num-max(dot-product(vec1, vec1), dot-product(vec2, vec2))
  
#|where:
  doc1 = [list: "a", "b", "c"]
  doc2 = [list: "d", "d", "d", "b"]


  overlap(doc1, doc2) is 1/3
  |#
end
