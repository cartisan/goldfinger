'''
Let's generate a story, shall we?
'''
from random import randint

from create_fabula import generate_story
from discourse import generate_partial_story, introduction, ending
from discourse_locations import generate_location_story
from discourse_connectors import get_connector

try:
    import numpy as np
    import matplotlib.pyplot as plt
    PLOT = True
except ImportError:
    pass


# scale 1-10
LOCATION_ADDING = 4


def die(i):
    return randint(0, i)


class Generator(object):
    '''
    Generate and embellish a story.

    Input: String name of story
    Output: String text; and a saved file called "storyName.txt"
        with the text.
    '''
    storyName = ''
    frame_story = []
    partial_story = []
    embellished_story = []
    tension_arc = []

    intro = ''
    end = ''

    def __init__(self, storyName):
        self.storyName = storyName
        self.frame_story = [] # F IS A TRIPLE (String, int, String)
        self.partial_story = [] # P IS A TUPLE (String, int)
        self.embellished_story = [] # E IS A TUPLE (String, int)

    def generate_frame(self):
        '''Generate skeleton'''
        self.frame_story = generate_story()

    def generate_tension_arc(self):
        '''Create tension arc from framework'''
        for bef_mid, tension, af_mid in self.frame_story:
            self.tension_arc.append(tension)
        print self.tension_arc
        if PLOT:
            self.make_plot()

    def generate_partial(self):
        '''Create partial sentences from the framework'''
        story_length = len(self.frame_story)
        for i in range(0, story_length):
            frame = self.frame_story[i]
            # check if last tuple
            if i == 0:
                self.intro = introduction(frame)[0]
                print self.intro
                frame = generate_partial_story(frame)
            elif i == story_length-1:
                self.end = ending(frame)[0]
                print self.end
                frame = generate_partial_story(frame, isLast=True)
            else:
                frame = generate_partial_story(frame)
            self.partial_story.append(frame)

    def generate_embellish(self):
        '''Add rubbish to the key partial sentences'''
        story_length = len(self.partial_story)
        for i in range(story_length):
            add_dot = True
            e = self.partial_story[i]
            if die(LOCATION_ADDING) == 0:
                add_dot = False
                e = generate_location_story(e)
            if die(LOCATION_ADDING) == 0:
                add_dot = False
                e = get_connector(e)
            if add_dot:
                text = e[0]
                tension = e[1]
                e = (text + '. ', tension)
            self.embellished_story.append(e)

    def generate(self):
        self.generate_frame()
        print 'FRAME'
        print self.frame_story
        self.generate_tension_arc()
        self.generate_partial()
        print 'PARTIAL'
        print self.partial_story
        self.generate_embellish()
        print 'EMBELLISHED'
        print self.embellished_story
        # export the story
        return self.export(self.embellished_story)

    def export(self, storyLst):
        '''
        Compile the story into a text.

        Input: list of tuples (String, int) storyLst
        Output: String text
        '''
        f = open(self.storyName + '.txt', 'w')
        # compile
        story = self.intro
        for textComp in storyLst:
            text = textComp[0]
            story += text + " \n"
        story += self.end
        f.write(story)
        return story

    def make_plot(self):
        # plot the tension arc
        x = np.array(range(len(self.tension_arc)))
        y = np.array(self.tension_arc)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y)
        axes = plt.gca()
        axes.set_ylim([0, 6])
        plt.title('Tension arc')
        plt.show()


if __name__ == '__main__':
    '''
    Get this shit going!!
    '''
    gen = Generator('fifth-story')
    gen.generate()

    # name = ''
    # gen = Generator(name)
    # gen.generate()
