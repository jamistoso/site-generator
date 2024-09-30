class HTMLNode:
    tag = None
    value = None
    children = None
    props = None
    
    def __init__(self, value=None, tag=None, children=None, props=None):
        self.value = value
        self.tag = tag
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        outStr = ''
        if self.props:
            for prop in self.props:
                outStr += ' ' + prop + '=' + self.props[prop]
        return outStr    

    def __repr__(self):
        outStr = ''
        outStr += f'Tag: {self.tag}\n'
        outStr += f'Value: {self.value}\n'
        outStr += f'Children: {self.children}\n'
        outStr += f'Props:{self.props_to_html()}'
        return outStr


class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(value, tag, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError('Leaf node has no value')
        if self.tag == None:
            return self.value
        outStr = ''
        outStr += f'<{self.tag}'
        outStr += self.props_to_html()
        outStr += f'>{self.value}</{self.tag}>'
        return outStr
    

class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(None, tag, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError('Parent node has no tag')
        if self.children == None or self.children == []:
            raise ValueError('Parent node has no children')
        outStr = f'<{self.tag}'
        outStr += self.props_to_html() + '>'
        for child in self.children:
            outStr += child.to_html()
        outStr += f'</{self.tag}>'
        return outStr
        