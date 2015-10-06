#!/usr/bin/python
__author__ = 'chukwuyem'
# quora.com/challenges#typeahead_search

import sys

class quoraItem:
    def __init__(self, type, id, score, data_string):
        self.type = type
        self.id = id
        self.score = score
        self.data_string = data_string

def subquery(q_string, d_string):
    q_string = q_string.lower()
    d_string = d_string.lower()
    q_is_in_d_string = False
    #is the set of whole tokens in query string a subset of the set of whole tokens in the data string
    if set(q_string.split(' ')).issubset(set(d_string.split(' '))):
        q_is_in_d_string = True
    if q_is_in_d_string:
        return q_is_in_d_string
    #if each token in query string is a sub token of a token in the data string i.e. D'Ang subtoken of D'Angelo
    else:
        q_list = q_string.split(' ')
        d_list = d_string.split(' ')
        counter = 0
        #pick a token in query string
        for x in q_list:
            x_subtoken_in_d_string = False
            #running it against every token in data string
            for y in d_list:
                #check if sub token
                if x in y:
                    x_subtoken_in_d_string = True
                    break
            if x_subtoken_in_d_string:
                counter += 1
        if counter == len(q_list):
            q_is_in_d_string = True
    return q_is_in_d_string


class quoraStack:
    def __init__(self):
        self.data = []

    #ADD command
    def push(self, item):
        self.data.append(item)
        self.data = sorted(self.data, key=lambda item: item.score)

    #DEL command
    def remove(self, id):
        for x in self.data:
            if x.id == id:
                del self.data[self.data.index(x)]
                break

    #QUERY command
    def query(self, n, query_str):
        result_list= []
        # finding all quoraItem that fit the query string
        [result_list.append(item) for item in self.data if subquery(query_str, item.data_string)]
        #sorts the list by score
        result_list = sorted(result_list, key=lambda item: item.score)[::-1]
        # printing the ids
        print ' '.join(str(x.id) for x in result_list[:n])

    def wquery(self, n, boost_str, query_str):
        result_list= []
        # finding all quoraItem that fit the query string
        #we append the [item, wq_score] to result_list which is initially 1
        #later on, we will multiple that 1 by all boosts that fit the item
        [result_list.append([item, 1]) for item in self.data if subquery(query_str, item.data_string)]
        #working on boosts
        boost_list = boost_str.split(' ')
        #each boost is in the form  'type/id:boost' so a result is boost
        #either by its type or id, so  I split each boost by ':' and check
        #each result if
        for boost in boost_list:
            for result in result_list:
                if boost.split(':')[0] == result[0].type or boost.split(':')[0] == result[0].id:
                    result[1] = result[0].score * float(boost.split(':')[1])
        #resorts the list by score
        result_list = sorted(result_list, key=lambda item: item[1])[::-1]
        # printing the ids
        print ' '.join(str(x[0].id) for x in result_list[:n])


#the main list that contains everything
processing_list = quoraStack()

def test():
    #the test main function
    #written so that each command is entered individually for test purposes
    num_commands = int(raw_input('Enter number of commands here -> '))
    while num_commands > 0:
        command = raw_input('Type command -> ')
        #list of all the spaces that occur in command
        #that way, each element of command is easily addressable
        li = [i for i,x in enumerate(command) if x == ' ']
        if command[:li[0]] == 'ADD':
            comm_item = quoraItem(command[ li[0]+1 : li[1] ], command[li[1]+1: li[2]],
                                  float(command[li[2]+1: li[3] ]), command[li[3]+1:])
            processing_list.push(comm_item)
        elif command[:li[0]] == 'DEL':
            processing_list.remove(command[li[0]+1 :])
        elif command[:li[0]] == 'QUERY':
            processing_list.query(int(command[li[0]+1 : li[1] ]), command[li[1]+1 :])
        elif command[:li[0]] == 'WQUERY':
            num_boost = int(command[li[1]+1 : li[2]])
            boost_string = command[li[2]+1 : li[num_boost + 2]]
            query_string = command[li[num_boost + 2]+1 :]
            processing_list.wquery(int(command[li[0]+1 : li[1] ]), boost_string, query_string)
        num_commands -= 1


def process_command(command_input):
    li = [i for i,x in enumerate(command_input) if x == ' ']
    if command_input[:li[0]] == 'ADD':
        comm_item = quoraItem(command_input[li[0]+1: li[1]], command_input[ li[1]+1: li[2]],
                              float(command_input[li[2]+1: li[3]]), command_input[li[3]+1:])
        processing_list.push(comm_item)
    elif command_input[:li[0]] == 'DEL':
        processing_list.remove(command_input[li[0]+1 :])
    elif command_input[:li[0]] == 'QUERY':
        processing_list.query(int(command_input[li[0]+1 : li[1] ]), command_input[li[1]+1 :])
    elif command_input[:li[0]] == 'WQUERY':
        num_boost = int(command_input[li[1]+1 : li[2]])
        boost_string = command_input[li[2]+1 : li[num_boost + 2]]
        query_string = command_input[li[num_boost + 2]+1 :]
        processing_list.wquery(int(command_input[li[0]+1 : li[1] ]), boost_string, query_string)

def main_function():
    if len(sys.argv) > 1:
        print str(sys.argv[1])
        f= open( str(sys.argv[1]), 'r')
        num_commands = int(f.readline())
        [process_command(l) for l in f.read().split('\n') if l]
    else:
        command_input = raw_input('')
        num_commands = int(command_input)
        while num_commands > 0:
            command_input = raw_input('')
            process_command(command_input)
            num_commands -= 1

main_function()