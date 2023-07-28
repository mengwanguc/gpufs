# How to study Pytorch source codes

## print

To me, the easist and most effective way to study source codes of a large system is just adding "printf":

```
while you are interested in some function/values:
    printf("Function xxx is called. Value of y is: %d", y);
    % or print the call stack of the function
    % of print something else
    read the output and source codes, and you are now interested in some other functions/variables 
```

I've been using this method to study the source codes of many systems including Linux kernel, MongoDB, Cassandra, OpenJDK, Pytorch, Filecoin, CORTX, .... These systems are written in different languages with different architectures, but all can be studied by simply using "printf".

Sometimes when you are studying function A, you might want to know who is calling A. To know it, you need to print call stack of function A. In Python, it can be done by adding:

```python
import trackback

# Who is calling function A?
def A():
    print("-- call stack of Function A")
    for line in traceback.format_stack():
        print(line.strip())
    print("---\n")
```

Sometimes, when you call function B, you want to know how B is implemented. In order to do so, you need to locate where B is implemented. Sometimes it's easy by simply searching for "def B(". 

Sometimes it's not that apparent. But in Python, you can locate B's implementation by using the `inspect` module. For example:

```python
import inspect

def A():
    # Who I'm calling
    file_path = inspect.getsourcefile(functionB)
    source_lines, starting_line_number = inspect.findsource(functionB)
    print("functionB is implemented in file: {}  starting_line_number: {}".format(file_path, starting_line_number))
    functionB()
```

## Comments

People's comments are useful. The developers added comments for you to understand their thoughts when they implement the codes. So do read the comments.

Sometimes the comments are long. When this happens, focus the comments that you feel are important for your task.

## Don't be afraid

Don't be afraid of reading system source codes... It's all about time commitment. As long as you spend enough time, you will learn it. And the process of learning is fun :)
