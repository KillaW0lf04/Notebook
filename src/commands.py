"""Available commands for the Notebook program are stored in this file"""
import os
import time

LINE_LIMIT = 75

def has_cmd(notebook, arg):
    """
    Checks if a word exists in the currently loaded notebook.
    """
    if arg:    
        print notebook.suffix_tree.has_word(arg.lower())
    else:
        print 'Argument expected'


def lswords_cmd(notebook, arg):
    """
    Lists all the unique words found in the currently loaded notebook (in
    alphabetical order). The command will only display whole words. To 
    include word suffixes in the results, use the '--all' argument.
    """
    include_suffixes = (arg == '--all')
    
    words = notebook.suffix_tree.words(include_suffixes)
    
    buffer = ''
    for word in words:
        if len(buffer) + len(word) + 1 < LINE_LIMIT:
            buffer += word + ', '
        else:
            print buffer
            buffer = ''
    
    print '(%s entries)' % len(words) 

     
def get_cmd(notebook, arg):
    """
    gets meta information from the specified word in the currently loaded notebook.
    """
    if arg:
        data = notebook.suffix_tree.get_data(arg.lower())
        if data: 
            for entry in data:
                print 'position=%s, whole_word=%s' % entry.meta
            
            print '(%s entries)' % len(data)
        else:
            print '\'%s\' not found' % arg
    else:
        print 'Argument expected'


def print_cmd(notebook, arg):
    """
    prints text from the currently loaded notebook. Can either print individual
    lines specified in the arguments using the line number, or the entire document
    can be printed using the '--all' argument.
    """
    # Naive implementation, needs to be improved
    if arg:      
        with open(notebook.file_path) as nfile:
            for line_no, line in enumerate(nfile.readlines()):
                if arg == '--all':
                    print line.rstrip()
                    continue
                
                try:
                    if line_no == int(arg):
                        print line.rstrip()
                        return
                except:
                    print 'Invalid Argument passed'
                    return
                
        if arg != 'all':
            print 'Unable to find specified line (%s)' % arg
    else:
        print 'Line Argument expected'

 
def reload_cmd(notebook, arg):
    """
    Loads the notebook with the specified file. Will reload the current file if no
    path is specified in the arguments.
    """
    if os.path.exists(arg):
        print 'Reloading %s (%s kb)' % (arg, os.path.getsize(arg)/1024)
        t0 = time.time()
        notebook.reload(arg)
         
        print 'Notebook reloaded with %s (in %.2f seconds)' % (notebook.file_path, time.time() - t0)
    else:
        print 'The path specified does not exist'
   
 
def show_cmd(notebook, arg):
    """
    Shows and prints all lines which have occurrences with the word specified in
    the argument.
    """
    if arg:
        data = notebook.suffix_tree.get_data(arg.lower())
        if data:
            lines = []
            for entry in data:  
                pos, _ = entry.meta
                _, y = pos
                lines.append(y)
                
            with open(notebook.file_path) as nfile:
                for line_no, line in enumerate(nfile.readlines()):
                    if line_no in lines:
                        print '(line %s) \'%s\'' % (line_no, line.rstrip())
                        
            print '(showing %s entries)' % len(lines)
        else:
            print '\'%s\' not found' % arg
    else:
        print 'Argument expected'          

    
def info_cmd(notebook, arg):
    """
    Displays information about the currently loaded notebook.
    """
    print 'file=[%s] with [%s] unique words' % (notebook.file_path, len(notebook.suffix_tree.words()))
    