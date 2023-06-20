more_lines = ['', 'Append text files', 'The End']

with open('readme.txt', 'a') as f:
    f.write('\n'.join(more_lines))