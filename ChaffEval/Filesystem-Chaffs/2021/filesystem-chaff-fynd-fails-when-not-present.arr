use context essentials2021
include shared-gdrive("filesystem-definitions.arr", "1Oesie_ZfHEVs9KTA9-QBY41ci0uKuHGI")

provide: how-many, du-dir, can-find, fynd end
# END HEADER
#| chaff (tdelvecc, Aug 31, 2020): 
    Raises an error in fynd when no file present with given name.
    Search "CHAFF DIFFERENCE" for changed code.
|#

import lists as lists

fun how-many(directory :: Dir) -> Number:
  doc: "Finds the number of files in the directory tree."
  # Fold over sub-directories, starting with number of files in current directory
  for fold(num-files from directory.fs.length(), sub-dir from directory.ds):
    num-files + how-many(sub-dir)
  end
end

fun du-dir(directory :: Dir) -> Number:
  doc: "Finds the total size of the directory tree."
  # Find size of files in current directory
  for fold(files-size from directory.fs.length(), a-file from directory.fs):
    files-size + a-file.size()
  end
  +
  # Find size of sub-directories in current directory
  for fold(directories-size from directory.ds.length(), a-dir from directory.ds):
    directories-size + du-dir(a-dir)
  end
end

fun can-find(directory :: Dir, name :: String) -> Boolean:
  doc: "Determines whether a file with given name is in the directory tree."
  # Check if it's in current directory
  for any(a-file from directory.fs):
    a-file.name == name
  end
  or
  # Check if it's in sub-directories
  for any(a-dir from directory.ds):
    can-find(a-dir, name)
  end
end

fun fynd(directory :: Dir, name :: String) -> List<Path>:
  doc: "Finds all instances of files with given name in the directory tree."
  sub-dir-paths :: List<Path> =
    directory.ds
    ^ map(fynd(_, name), _) # Recur on sub-dirs
    ^ fold(lists.append, empty, _) # Combine results into one list
    ^ map(link(directory.name, _), _) # Add current directory to paths
  
  # If file is in current directory, add new path
  if directory.fs.map(_.name).member(name):
    link([list: directory.name], sub-dir-paths)
    # CHAFF DIFFERENCE: Raises error when file not found
  else if is-empty(sub-dir-paths):
    raise("Fild not found.")
  else:
    sub-dir-paths
  end
end