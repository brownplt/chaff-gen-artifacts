use context essentials2021

provide: overlap end
# END HEADER
#|
    DOES NOT obey:
        Overlap of two documents must be proportional to the dot product of the documents
    Instead: Always returns an overlap of 0
|#
import lists as lists

fun overlap(doc1 :: List<String>%(is-link), doc2 :: List<String>%(is-link)) -> Number:
  doc: "Finds the overlap value of two documents."
  
  0
end
  
