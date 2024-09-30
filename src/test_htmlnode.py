import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq1(self):
        tag1 = 'a'
        value1 = '1'
        props1 = {'a': 'b'}
        node = HTMLNode(value1, tag1, None, props1)
        self.assertEqual(node.tag, tag1)
        self.assertEqual(node.value, value1)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, props1)

    def test_eq2(self):
        children1 = ['heh']
        node = HTMLNode(None, None, children1, None)
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, children1)
        self.assertEqual(node.props, None)

    def test_repr(self):
        value1 = '1'
        props1 = {'a': 'b'}
        node = HTMLNode(value1, None, None, props1)
        to_str_html = repr(node)
        expected = 'Tag: None\nValue: 1\nChildren: None\nProps: a=b'
        self.assertEqual(to_str_html, expected)


class TestLeafNode(unittest.TestCase):
    tag1 = 'a'
    value1 = '1'
    children1 = ['heh']
    props1 = {'a': 'b'}
    tag2 = 'b'
    value2 = '2'
    children2 = ['hah']
    props2 = {'c': 'd'}
    
    def test_value_exists(self):
        node = LeafNode(None, None, None)
        self.assertRaises(ValueError, node.to_html)
        node = LeafNode('value', None, None)
        self.assertEqual(node.to_html(), 'value')

    def test_to_html(self):
        node = LeafNode('value', None, None)
        self.assertEqual(node.to_html(), 'value')
        node = LeafNode('value', 'a', None)
        self.assertEqual(node.to_html(), '<a>value</a>')
        node = LeafNode('value', 'a', {'b':'c', 'd':'e'})
        self.assertEqual(node.to_html(), '<a b=c d=e>value</a>')


class TestParentNode(unittest.TestCase):
    tag1 = 'a'
    children1 = ['heh']
    props1 = {'a': 'b'}
    tag2 = 'b'
    children2 = ['hah']
    props2 = {'c': 'd'}
    
    def test_tag_children_exists(self):
        node = ParentNode(None, None, None)
        self.assertRaises(ValueError, node.to_html)
        node = ParentNode(None, "a", None)
        self.assertRaises(ValueError, node.to_html)
        node = ParentNode([LeafNode('c', 'b')], "a", None)
        self.assertEqual(node.to_html(), '<a><b>c</b></a>')

    def test_to_html(self):
        node = ParentNode(
            [
                LeafNode("Bold text", "b"),
                LeafNode("Normal text", None),
                LeafNode("italic text", "i"),
                LeafNode("Normal text", None),
            ],
            "p"
        )

        expected = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(expected, node.to_html())

    def test_nested_parent(self):
        node = ParentNode(
            [
                ParentNode([
                    LeafNode('Leaf value', 'c')
                ], "b")
            ],
            "a"
        )

        expected = '<a><b><c>Leaf value</c></b></a>'
        self.assertEqual(node.to_html(), expected)

if __name__ == "__main__":
    unittest.main()
