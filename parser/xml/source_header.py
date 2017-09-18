import re


class SourceHeader(object):

    @classmethod
    def get_source_header(cls, parsed_xml, header):

        # iterate through every item of list in marc21 key of input Dictionary
        for attr in header:
            found = parsed_xml.xpath(header[attr]['path'])

            # assing value of attribute from found item
            header[attr]['value'] = cls.__clean_and_join_list(found)

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
