import turtle
import tkinter


# Simple graphic helper class mainly build for testing correctness of steps
# of preprocessing of xml data for articles
class Graphic(object):
    @classmethod
    def draw_elem_network(cls, page, attrs):
        """
        simply draws certain elements from page, the chosen elements
        must have coordinates attributes, for real example, check
        test in helper dir with name test_graphic

        :param
        page: lxml element, schould contain only 1 page
        attrs: Dictionary, includes Hashes with 2 keys:
            elem_path - String xpath format, example: '//par'
            attrib - Array of Strings, String value represents name
                of element attribute, example: ['type', 'l', 'r']
        """
        devider = 1

        boom = turtle.Turtle()
        boom.speed(10)
        screen = boom.getscreen()
        screen.setup(800, 1000)
        # boom.setup(1000, 1000)
        screen.reset()
        # screen.setworldcoordinates(3500, 6500, 10, 10)
        # screen.setworldcoordinates(3500, 10, 10, 6500)
        screen.setworldcoordinates(0, 6500, 4000, 0)
        # screen.setworldcoordinates(0, 6500, 6500, 0)
        screen.tracer(0)
        screen.update()

        for attr in attrs:
            elem_path = attr['elem_path']
            attrib = attr['attrib']

            for elem in page.xpath(elem_path):
                l = int(elem.attrib['l']) / devider
                t = int(elem.attrib['t']) / devider
                r = int(elem.attrib['r']) / devider
                b = int(elem.attrib['b']) / devider
                height = b - t
                width = r - l

                boom.penup()
                boom.setposition(l, b)
                boom.down()

                # write desired attrib values
                s = ''
                for attr in attrib:
                    s += attr + ': ' + str(elem.attrib.get(attr)) + ', '
                boom.write(s)

                # rectangle
                # for i in range(2):
                    # boom.forward(width)
                    # boom.left(90)
                    # boom.forward(height)
                    # boom.left(90)
                boom.goto(l, t)
                boom.goto(r, t)
                boom.goto(r, b)
                boom.goto(l, b)

        boom.penup()
        screen.mainloop()

    @classmethod
    def draw_articles(cls, articles, dir_path):
        """
        Firstly initialize Semantic which parses xml and
        then call this static method for generating images.
        Simple use, check method test_draw_single_page_groups
        in test test_graphic.py in tests/helper.

        :param articles: instance attribute of Semantic class
        after Semantic initialization
        :param dir_path: String, desired directory path where should
        this method save all pictures representing all pages
        in parsed xml document
        :return:
        """
        boom = turtle.Turtle()
        boom.speed(10)
        screen = boom.getscreen()
        screen.setup(800, 1000)
        screen.reset()
        screen.setworldcoordinates(0, 6500, 4000, 0)
        screen.tracer(0)
        screen.update()
        article_num = 0

        for page_index, page in enumerate(articles):
            for article_index, article in enumerate(page):
                article_num += 1
                for group_index, group in enumerate(article):
                    l = int(group.attrib['l'])
                    t = int(group.attrib['t'])
                    r = int(group.attrib['r'])
                    b = int(group.attrib['b'])

                    # write article number of group
                    boom.penup()
                    boom.setposition(l, t)
                    boom.down()
                    boom.pencolor('red')
                    boom.write('AN: ' + str(article_num), font=("Arial", 8, "bold"))

                    # write type og group
                    boom.penup()
                    boom.setposition(l + 200, t)
                    boom.down()
                    boom.pencolor('blue')
                    boom.write('type: ' + group.attrib['type'].upper(), font=("Arial", 8, "bold"))

                    boom.pencolor('black')

                    # write text in group
                    for par in group.xpath('par'):
                        for line in par.xpath('line'):
                            ln = ''
                            for formatting in line.xpath('formatting'):
                                ln += formatting.text

                            l_line = int(line.attrib['l'])
                            b_line = int(line.attrib['b'])
                            boom.penup()
                            boom.setposition(l_line + 15, b_line)
                            boom.down()
                            boom.write(ln, font=("Arial", 6, "normal"))

                    # draw rectangle of group
                    boom.penup()
                    boom.setposition(l, b)
                    boom.down()

                    boom.goto(l, t)
                    boom.goto(r, t)
                    boom.goto(r, b)
                    boom.goto(l, b)

            boom.penup()

            # save page in file
            screen.getcanvas().postscript(file=dir_path + '/' + str(page_index + 1) + '.eps')

            screen.clear()
            boom.speed(10)
            screen = boom.getscreen()
            screen.setup(800, 1000)
            screen.reset()
            screen.setworldcoordinates(0, 6500, 4000, 0)
            screen.tracer(0)
            screen.update()


