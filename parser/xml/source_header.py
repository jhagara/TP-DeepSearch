import re


class SourceHeader(object):

    @classmethod
    def get_source_header(cls, parsed_xml, header):
        blocks = []

        # iterate through every item of list in marc21 key of input Dictionary
        for attr in header["marc21"]:
            found = parsed_xml.xpath(attr['path'])

            # assing value of attribute from found item
            attr['value'] = cls.__clean_and_join_list(found)

            # find block ancestor and push it to array
            if attr['value'] is not None:
                block = cls.__iterate_ancestors(found[0])
                if block is not None:
                    blocks.append(block)

        # delete all used blocks
        for block in blocks:
            try:
                block.getparent().remove(block)
            except:
                None

        return parsed_xml, header

    # just list cleaner, join list of strings and
    # clean string (remove all non-printable characters)
    @classmethod
    def __clean_and_join_list(cls, list):
        if (len(list) != 0):
            return re.sub("[\a\f\n\r\t\v]", '', ''.join(list))
        else:
            return None

    # recursively go through all ancestors - parents
    @classmethod
    def __iterate_ancestors(cls, elem):
        if elem is None or \
                (elem.__class__.__name__ == '_Element' and
                 elem.tag == 'block'):
            return elem
        else:
            return cls.__iterate_ancestors(elem.getparent())
