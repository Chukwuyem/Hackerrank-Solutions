#!/usr/bin/python
__author__ = 'chukwuyem'
#www.quora.com/challenges#feed_optimizer

import sys

class feed_story:
    def __init__(self, publication_time, score, pixel_height, id_num):
        self.publication_time = publication_time
        self.score = score
        self.pixel_height = pixel_height
        self.id_num = id_num

#storage
main_list_of_stories =[]



def generate_possible_feeds(story_list, max_pixel_height,  partial, possible_feed_list):
    '''generates all possible combinations of stories that can fit
    into feed'''

    #sum of partial... i.e. s = sum(partial)
    s = sum(a.pixel_height for a in partial)

    # check if the partial sum is equals to target...
    #i.e. check is sum of pixels of stories in partial sum is less than or equal to max pixel height
    if s <= max_pixel_height:
        if len(partial) != 0: possible_feed_list.append(partial)
        #print "feed(%s) with height %s can fit in %s pixels" % ([sty.id_num for sty in partial], s, max_pixel_height)
        #print "sum(%s) less than or equal %s" % (partial, max_pixel_height)
    if s >= max_pixel_height:
        return  # if we reach the number why bother to continue

    for i in range(len(story_list)):
        n = story_list[i]
        remaining = story_list[i+1:]
        generate_possible_feeds(remaining, max_pixel_height, partial + [n], possible_feed_list)




def reload_function(time_of_reload, recent_event_age, max_pixels):
    #removing old stories since they won't be used again
    for story in main_list_of_stories:
        if time_of_reload - story.publication_time > recent_event_age:
            del main_list_of_stories[main_list_of_stories.index(story)]

    possible_feeds_list = [] #possible feeds that fit the users browser window
    working_partial_list = []
    generate_possible_feeds(main_list_of_stories, max_pixels, working_partial_list, possible_feeds_list)
    #now, the possible_feeds_list is filled

    #sorting the list based on total score of each feed
    possible_feeds_list_sorted = sorted(possible_feeds_list, key= lambda feed_: sum(stu.score for stu in feed_))

    feeds_with_highest_score = []
    #highest score is the score of the feed at the end of the list
    highest_score = sum(s.score for s in possible_feeds_list_sorted[len(possible_feeds_list_sorted) - 1])

    #adding any feed with the score equal to highest score to the feed_with_top_score list
    #[feeds_with_highest_score.append(feed) for feed in possible_feeds_list_sorted
    # if sum(sty.score for sty in feed) == highest_score]

    #a faster way so it doesn't have to traverse the whole list, knowing that the top scores are at the edge of the list
    #we run the list backwards, once a smaller score is encountered, break
    for feed in possible_feeds_list_sorted[::-1]:
        if sum(sty.score for sty in feed) == highest_score: feeds_with_highest_score.append(feed)
        else: break


    #if only one feed has the top score
    if len(feeds_with_highest_score)== 1 :
        #remember, the output is score, number of stories, each story id_num
        print highest_score, len(feeds_with_highest_score[0]), \
            ' '.join(str(sto.id_num) for sto in feeds_with_highest_score[0])

    else:
        #sorting the feeds with highest score according to number of stories
        feeds_with_highest_score_sorted = sorted(feeds_with_highest_score, key=lambda feed: len(feed))

        #printing feed with the least number of stories if only one such feed exists
        if len(feeds_with_highest_score_sorted[0]) < len(feeds_with_highest_score_sorted[1]):
            print highest_score, len(feeds_with_highest_score_sorted[0]), \
                ' '.join(str(sto.id_num) for sto in feeds_with_highest_score_sorted[0])

        #else, printing the lexicographically smallest feed using id_nums
        else:
            smallest_len = len(feeds_with_highest_score_sorted[0])
            feeds_highest_score_least_stories= []
            #it appends the list of id_nums of each story in the feed for each feed
            #so you list = [ [list of id_nums_1], [list of id_nums_2], .... , [list of id_nums_n]]
            [feeds_highest_score_least_stories.append([st.id_num for st in feed])
             for feed in feeds_with_highest_score_sorted if len(feed)== smallest_len]
            #sorting them in lexicographical order
            feeds_highest_score_least_stories.sort(key=str)
            print highest_score, len(feeds_highest_score_least_stories[0]), \
                ' '.join(str(stry.id_num) for stry in feeds_highest_score_least_stories[0])




def test():
    story_id_num_iterator = 0
    general_params = raw_input('Enter first line here-> ').split(' ')
    num_of_commands = int(general_params[0])
    time_window_recent = int(general_params[1])
    height_of_browser_pixels = int(general_params[2])
    while num_of_commands > 0:
        command = raw_input('Enter command here-> ').split(' ')
        if command[0] == 'S':
            story_id_num_iterator += 1
            new_story = feed_story(int(command[1]), int(command[2]), int(command[3]), story_id_num_iterator)
            main_list_of_stories.append(new_story)
        if command[0] == 'R':
            reload_function(int(command[1]), time_window_recent, height_of_browser_pixels)
        num_of_commands -= 1

def story_command(command_list, story_id_num):
    new_story = feed_story(int(command_list[1]), int(command_list[2]), int(command_list[3]), story_id_num)
    main_list_of_stories.append(new_story)


def main_function():
    story_id_num_iterator = 0
    if len(sys.argv) > 1:
        print str(sys.argv[1])
        f= open( str(sys.argv[1]), 'r')
        general_params = f.readline().split(' ')
        #num_commands = int(general_params[0])
        time_window_recent = int(general_params[1])
        height_of_browser_pixels = int(general_params[2])
        for command in f.read().split('\n'):
            if command: #to catch EOF and any non lines
                if command.split(' ')[0] == 'S':
                    story_id_num_iterator += 1
                    story_command(command.split(' '), story_id_num_iterator)
                elif command.split(' ')[0] == 'R':
                    reload_function(int(command.split(' ')[1]), time_window_recent, height_of_browser_pixels)
    else:
        #general_params = raw_input('Paste input here-> ').split(' ')
        general_params = raw_input('').split(' ')
        num_commands = int(general_params[0])
        time_window_recent = int(general_params[1])
        height_of_browser_pixels = int(general_params[2])
        while num_commands > 0:
            command_input = raw_input('')
            if command_input.split(' ')[0] == 'S':
                story_id_num_iterator += 1
                story_command(command_input.split(' '), story_id_num_iterator)
            elif command_input.split(' ')[0] == 'R':
                reload_function(int(command_input.split(' ')[1]), time_window_recent, height_of_browser_pixels)
            num_commands -= 1

main_function()