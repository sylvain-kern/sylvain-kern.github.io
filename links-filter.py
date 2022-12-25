'''working!!!
'''

from pandocfilters import toJSONFilters, Link
import json

extension = '.html'

def generate_link_dict(key, value, format, meta):
    '''passes through the doc and fills LinkDict = {link of header hn | link of h1 or h2 that contains hn}
        needs to take references from image, table, eq links
    '''

    global LinkDict
    with open('./linkdict.json') as dictfile:
        LinkDict = json.load(dictfile)
    global currentFileLabel

    if key == 'Header':
        [level, [label, t1, t2], header] = value
        if level <= 2:
            currentFileLabel = label
            LinkDict[label] = label
        else:
            LinkDict[label] = currentFileLabel

    # if key == 'Para' and len(value) == 1 and \
    #     value[0]['t'] == 'Image' and value[0]['c'][-1][1].startswith('fig:'):
    #     label = value[0]['c'][0][0]
    #     LinkDict[label] = currentFileLabel

    if key in ('Table', 'Image'):
        label = value[0][0]
        LinkDict[label] = currentFileLabel

    with open('linkdict.json', 'w') as convert_file:
        convert_file.write(json.dumps(LinkDict))

def set_links(key, value, format, meta):
    '''for all links, detects if it points to an header (contained in LinkDict), and replaces with the good link
    ok
    '''

    global currentFileLabel

    with open('./linkdict.json') as dictfile:
        LinkDict = json.load(dictfile)

    if format == 'html':
        if key == 'Header':
            [level, [label, t1, t2], header] = value
            if level <= 2:
                currentFileLabel = label

        if key == 'Link':
            [t1, linktext, [href, t4]] = value
            if href[1:] in LinkDict:
                if LinkDict[href[1:]] != currentFileLabel:
                    newhref = LinkDict[href[1:]]+'.html'+href
                    return Link(t1, linktext, [newhref, t4])



if __name__=='__main__':
    toJSONFilters([generate_link_dict, set_links])