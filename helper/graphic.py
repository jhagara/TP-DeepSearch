import turtle


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
