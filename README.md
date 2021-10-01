# Git Tree

Display the working-directory git status, in a tree-format.

## Inner Workings

Jumpstarted by a bash script, which ensures the target is a git-versioned directory.
In the case of success, `git status --porcelain` is executed, and piped to the python script's standard input stream.

The py script then leverages the standard format to split each entry into a status and path.
For each entry, the path is placed in a tree, removing duplicated parental directories and yielding the file's status at the leaf nodes.
This tree is then iterated over; each directory name is printed and an appriopriate prefix is prepended to descendants.
Finally, the leaf-nodes, which are git-versioned files, are displayed in a visually-appropriate manner.
