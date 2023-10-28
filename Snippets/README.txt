Snippets>h
> [help] (h)              |                                                     | Get help

> [create_files] (cf)     | (trailing:string)                                   | Given [names], creates files at context

> [delete_files] (df)     | (trailing:string)                                   | Given [names], deletes files from context and prints content

> [rename_file] (rf)      | (string:None)(string:None)                          | Given a [old file] and [new name], will rename the old file

> [edit_file] (ef)        | (string:None)(boolean:false)                        | Given a [name] and whether to [create if nonexistent], will open a text editor to edit the file

> [append_file] (af)      | (string:None)(boolean:false)(string:Unnamed Entry)  | Given a [name], whether to [create if nonexistent], and an [entry title], will append a titled entry, gotten from a text editor, to the specified file

> [modify_file] (mf)      | (string:None)(boolean:false)(boolean:false)(string:)| Given a [name], whether to [create if nonexistent], whether to [append], and (optionally) the [entry name]. Essentially a multipurpose file tool that combines the functionality of edit_file and append_file

> [print_files] (pf)      | (trailing:string)                                   | Given a [name], prints the contents of that file

> [advance_context] (ac)  | (string:None)                                       | Given a [directory], will advance the working directory inside it

> [recede_context] (rc)   |                                                     | Pops the last directory off of the working directory

> [print_context] (pc)    |                                                     | Prints the current working directory

> [list_context] (lc)     |                                                     | Prints out the contents of the working directory

> [walk_context] (wc)     |                                                     | Recursively prints out the entirety of the working directory tree

> [create_dirs] (cd)      | (trailing:string)                                   | Given [names], will create a new directory for each, skipping already existing

> [delete_dirs] (dd)      | (trailing:string)                                   | Given [names], will delete each directory recursively and the contents of each deleted file

> [rename_dir] (rd)       | (string:None)(string:None)                          | Given a [old dir] and a [new name], will rename the dir with a new name

> [print_dirs] (pd)       | (boolean:False)(trailing:string)                    | Given whether to [print recursively] and a list of [dirs] to print, will print the contents of each dir

> [create_bookmark] (cb)  | (string:None)                                       | Given a [name], will create a new bookmark located at current working directory

> [delete_bookmarks] (db) | (trailing:string)                                   | Given a [name], will delete that bookmark

> [rename_bookmark] (rb)  | (string:None)(string:None)                          | Given an [old name] and a [new name], will rename the old bookmark with a new name, preserving the location

> [edit_bookmark] (eb)    | (string:None)(string:None)                          | Given a [name] and [new location], will change the location of the bookmark

> [print_bookmarks] (pb)  | (trailing:string)                                   | Given [names], will print the names and locations of each bookmark

> [list_bookmarks] (lb)   |                                                     | Prints the names and locations of each bookmark you have

> [goto_bookmark] (gb)    | (string:None)                                       | Given a [name], will set the current working directory to the bookmarks location

> [set_bookmark] (sb)     | (string:None)                                       | Given a [name], the bookmarks location will be updated to the current working directory
