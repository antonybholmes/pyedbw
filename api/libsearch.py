import re
from api import libcollections

class SearchStackElem(object):
    def __init__(self, op, text=''):
        self.__op = op
        self.__text = text

    @property
    def op(self):
        return self.__op
    
    @property
    def text(self):
        return self.__text
        

def parse_query(q):
    """
    Implementation of shunting yard for creating boolean queries
    
    Parameters
    ----------
    q : str
        String query. If query contains uppercase 'AND' or 'OR' these
        will be treated as boolean operators.
        
    Returns
    -------
    array
        Query parsed into array form for evaluation.
    """
    
    # extract all word tokens and then recreate string to eliminate
    # garbage input
    q = ' '.join(re.findall(r'(\w+)', q))
    
    q = q.replace(" ", " AND ")
    q = q.replace("AND OR AND", "OR")
    q = q.replace("AND AND AND", "AND")
    q = q.replace("  ", " ")
    
    buffer = ''
    op_stack = libcollections.Stack()
    output_queue = []
    
    for c in q:
        if c == '(':
            add_term(buffer, output_queue)
            op_stack.push(c)
            buffer = ''
        elif c == ')':
            add_term(buffer, output_queue)
            right_parens(output_queue, op_stack)
            buffer = ''
        elif c == ' ':
            add_term(buffer, output_queue)
            buffer = ''
        else:
            buffer += c

            if c == 'D':
                if buffer == 'AND':
                    add_lower_precedence_ops('AND', output_queue, op_stack)
            
                    buffer = ''
            elif c == 'R':
                if buffer == 'OR':
                    add_lower_precedence_ops('OR', output_queue, op_stack)
            
                    buffer = ''
            else:
                pass

    # add any remaining operators onto the queue
    add_term(buffer, output_queue)

    while len(op_stack) > 0:
        output_queue.append(SearchStackElem(op_stack.pop()))
        
    return output_queue
    

def add_term(buffer, output_queue):
    s = buffer.lower()

    if len(s) > 0:
      output_queue.append(SearchStackElem('MATCH', s))


def add_lower_precedence_ops(op1, output_queue, op_stack):
    p1 = precedence(op1)

    # Look for ops with greater presedence since we want to evaluate
    # AND before OR

    while len(op_stack) > 0:
        op2 = op_stack.peek()

        if p1 > precedence(op2):
            break

        # We have encountered two 'and' statements for example
        output_queue.add(SearchStackElement(op2))

        # remove the operator as we have dealt with it
        op_stack.pop()

    # Add the new operator to the op stack
    op_stack.push(op1)

 
def right_parens(output_queue, op_stack):
    # deal with existing op_stack

    while len(op_stack) > 0:
        op2 = op_stack.pop()

        if op2 == '(':
            break

        output_queue.add(SearchStackElement(op2))
        
  
def precedence(op):
    if op == 'NOT':
        return 4
    elif op == 'AND' or op == 'NAND':
        return 3
    elif op == 'OR' or op == 'XOR':
        return 2
    else:
        return -1
