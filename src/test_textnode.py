import unittest

from delimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", "bold", "link")
        node2 = TextNode("This is a text node", "bold", "link")
        self.assertEqual(node, node2)

    def test_eq_url_none(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text nod", "bol", "uh")
        node2 = TextNode("This is a text node", "bold", None)
        self.assertNotEqual(node, node2)


class TestTextToHTML(unittest.TestCase):
    def test_invalid_type(self):
        node = TextNode('invalid node', 'invalid', None)
        self.assertRaises(Exception, text_node_to_html_node, node)

    def test_text_type(self):
        node = TextNode('text node', 'text', None)
        expectedNode = LeafNode('text node', None, None)
        returnedNode = text_node_to_html_node(node)
        self.assertEqual(returnedNode.tag, expectedNode.tag)
        self.assertEqual(returnedNode.value, expectedNode.value)

    def test_bold_type(self):
        node = TextNode('text node', 'bold', None)
        expectedNode = LeafNode('text node', 'b', None)
        returnedNode = text_node_to_html_node(node)
        self.assertEqual(returnedNode.tag, expectedNode.tag)
        self.assertEqual(returnedNode.value, expectedNode.value)

    def test_italic_type(self):
        node = TextNode('text node', 'italic', None)
        expectedNode = LeafNode('text node', 'i', None)
        returnedNode = text_node_to_html_node(node)
        self.assertEqual(returnedNode.tag, expectedNode.tag)
        self.assertEqual(returnedNode.value, expectedNode.value)

    def test_code_type(self):
        node = TextNode('text node', 'code', None)
        expectedNode = LeafNode('text node', 'code', None)
        returnedNode = text_node_to_html_node(node)
        self.assertEqual(returnedNode.tag, expectedNode.tag)
        self.assertEqual(returnedNode.value, expectedNode.value)

    def test_link_type(self):
        node = TextNode('text node', 'link', 'test_link')
        expectedNode = LeafNode('text node', 'a', {'href': 'test_link'})
        returnedNode = text_node_to_html_node(node)
        self.assertEqual(returnedNode.tag, expectedNode.tag)
        self.assertEqual(returnedNode.value, expectedNode.value)
        self.assertEqual(returnedNode.children, expectedNode.children)

    def test_image_type(self):
        node = TextNode('img node', 'image', 'test_link')
        expectedNode = LeafNode('', 'img', {'src': 'test_link', 'alt': 'img node'})
        returnedNode = text_node_to_html_node(node)
        self.assertEqual(returnedNode.tag, expectedNode.tag)
        self.assertEqual(returnedNode.value, expectedNode.value)
        self.assertEqual(returnedNode.children, expectedNode.children)


class TestSplitDelimiter(unittest.TestCase):

    def test_non_matching(self):
        node = TextNode('testing an *unmatched word','text', None)
        self.assertRaises(Exception, split_nodes_delimiter, [node], '*', 'bold')
        node = TextNode('testing an **unmatched word','text', None)
        self.assertRaises(Exception, split_nodes_delimiter, [node], '**', 'italic')

    def test_invalid_type(self):
        node = TextNode('testing an **invalid** type','text', None)
        self.assertRaises(Exception, split_nodes_delimiter, [node], '*', 'invalid')

    def test_invalid_node(self):
        node = TextNode('testing an **invalid** type','invalid', None)
        self.assertRaises(Exception, split_nodes_delimiter, [node], '**', 'italic')

    def test_bold(self):
        node = TextNode('testing a *bold* word','text', None)
        new_nodes = split_nodes_delimiter([node], '*', 'bold')
        expected = [
            TextNode('testing a ', 'text'),
            TextNode('bold', 'bold'),
            TextNode(' word', 'text')
        ]
        self.assertEqual(new_nodes, expected)
        
    def test_italic(self):
        node = TextNode('testing an **italic** word','text', None)
        new_nodes = split_nodes_delimiter([node], '**', 'italic')
        expected = [
            TextNode('testing an ', 'text'),
            TextNode('italic', 'italic'),
            TextNode(' word', 'text')
        ]
        self.assertEqual(new_nodes, expected)

    def test_code(self):
        node = TextNode('testing a `code` word','text', None)
        new_nodes = split_nodes_delimiter([node], '`', 'code')
        expected = [
            TextNode('testing a ', 'text'),
            TextNode('code', 'code'),
            TextNode(' word', 'text')
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple(self):
        node = TextNode('testing *multiple* bold *words*','text', None)
        new_nodes = split_nodes_delimiter([node], '*', 'bold')
        expected = [
            TextNode('testing ', 'text'),
            TextNode('multiple', 'bold'),
            TextNode(' bold ', 'text'),
            TextNode('words', 'bold'),
            TextNode('', 'text')
        ]
        self.assertEqual(new_nodes, expected)


class TestExtract(unittest.TestCase):
    def test_empty(self):
        text = ''
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])

    def test_link(self):
        text = '[a](b)'
        expected = [('a','b')]
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = 'Testing with [one link](link_one) and [another link](link_two)'
        expected = [('one link', 'link_one'), ('another link', 'link_two')]
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), expected)

    def test_images(self):
        text = '![a](b)'
        expected = [('a','b')]
        self.assertEqual(extract_markdown_images(text), expected)
        self.assertEqual(extract_markdown_links(text), [])

    def test_multiple_images(self):
        text = 'Testing with ![one image](image_one) and ![another image](image_two)'
        expected = [('one image', 'image_one'), ('another image', 'image_two')]
        self.assertEqual(extract_markdown_images(text), expected)
        self.assertEqual(extract_markdown_links(text), [])

    def test_multiple_images(self):
        text = 'Testing with ![one image](image) and [one link](link)'
        expected_image = [('one image', 'image')]
        expected_link = [('one link', 'link')]
        self.assertEqual(extract_markdown_images(text), expected_image)
        self.assertEqual(extract_markdown_links(text), expected_link)


class TestSplitImages(unittest.TestCase):
    def test_image(self):
        node = TextNode('testing a ![test](image) word','text', None)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode('testing a ', 'text'),
            TextNode('test', 'image', 'image'),
            TextNode(' word', 'text')
        ]
        self.assertEqual(new_nodes, expected)

        
    def test_multiple_images(self):
        test_text = 'testing a ![test](image) word and ![second test](image_two) word'
        node = TextNode(test_text, 'text', None)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode('testing a ', 'text'),
            TextNode('test', 'image', 'image'),
            TextNode(' word and ', 'text'),
            TextNode('second test', 'image', 'image_two'),
            TextNode(' word', 'text'),
        ]
        self.assertEqual(new_nodes, expected)

    def test_mix(self):
        test_text = 'testing a ![test](image) word and [test](link) word'
        node = TextNode(test_text, 'text', None)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode('testing a ', 'text'),
            TextNode('test', 'image', 'image'),
            TextNode(' word and [test](link) word', 'text'),
        ]
        self.assertEqual(new_nodes, expected)


class TestSplitLinks(unittest.TestCase):
    def test_link(self):
        node = TextNode('testing a [test](link) word','text', None)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode('testing a ', 'text'),
            TextNode('test', 'link', 'link'),
            TextNode(' word', 'text')
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_links(self):
        test_text = 'testing a [test](link) word and [second test](link_two) word'
        node = TextNode(test_text, 'text', None)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode('testing a ', 'text'),
            TextNode('test', 'link', 'link'),
            TextNode(' word and ', 'text'),
            TextNode('second test', 'link', 'link_two'),
            TextNode(' word', 'text'),
        ]
        self.assertEqual(new_nodes, expected)

    def test_mix(self):
        test_text = 'testing a ![test](image) word and [test](link) word'
        node = TextNode(test_text, 'text', None)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode('testing a ![test](image) word and ', 'text'),
            TextNode('test', 'link', 'link'),
            TextNode(' word', 'text'),
        ]
        self.assertEqual(new_nodes, expected)

    def test_link_end(self):
        node = TextNode('testing a [test](link)','text', None)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode('testing a ', 'text'),
            TextNode('test', 'link', 'link')
        ]
        self.assertEqual(new_nodes, expected)

        
    def test_link_begin(self):
        node = TextNode('[test](link) test','text', None)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode('test', 'link', 'link'),
            TextNode(' test', 'text', None)
        ]
        self.assertEqual(new_nodes, expected)


class TestConverter(unittest.TestCase):
    def test_converter(self):
        test_text = 'This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        text_type_text = 'text'
        text_type_bold = 'bold'
        text_type_italic = 'italic'
        text_type_code = 'code'
        text_type_image = 'image'
        text_type_link = 'link'
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        new_nodes = text_to_textnodes(test_text)
        self.assertEqual(expected, new_nodes)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_function(self):
        test_text = '''# This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block\n* This is a list item\n* This is another list item
        '''
        expected = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '''* This is the first list item in a list block\n* This is a list item\n* This is another list item'''
        ]
        self.assertEqual(markdown_to_blocks(test_text), expected)

    
    def test_whitespace(self):
        test_text = '''# This is a heading        

        


            This is a paragraph of text. It has some **bold** and *italic* words inside of it.
         '''
        expected = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.'
        ]
        self.assertEqual(markdown_to_blocks(test_text), expected)
        
class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        text = '# is a comment'
        expected = 'heading'
        self.assertEqual(block_to_block_type(text), expected)
        text = '###### is a comment'
        expected = 'heading'
        self.assertEqual(block_to_block_type(text), expected)
        text = '####### is not a comment'
        expected = 'paragraph'
        self.assertEqual(block_to_block_type(text), expected)
        text = '#also is not a comment'
        expected = 'paragraph'
        self.assertEqual(block_to_block_type(text), expected)

    def test_code(self):
        text = '```this is a code block```'
        expected = 'code'
        self.assertEqual(block_to_block_type(text), expected)
        text = '``this is not a code block```'
        expected = 'paragraph'
        self.assertEqual(block_to_block_type(text), expected)
    
    def test_quote(self):
        text = '> this is a\n> quote\n> block'
        expected = 'quote'
        self.assertEqual(block_to_block_type(text), expected)
        text = '> this is\n> not a\nquote block'
        expected = 'paragraph'
        self.assertEqual(block_to_block_type(text), expected)

    def test_unordered_list(self):
        text = '* this is an\n* unordered\n* list'
        expected = 'unordered_list'
        self.assertEqual(block_to_block_type(text), expected)
        text = '* this is\n* not an\nunordered list'
        expected = 'paragraph'
        self.assertEqual(block_to_block_type(text), expected)
        text = '* this is also\n* not an\n*unordered list'
        expected = 'paragraph'
        self.assertEqual(block_to_block_type(text), expected)

    def test_unordered_list_two(self):
        text = '- this is an\n- unordered\n- list'
        expected = 'unordered_list'
        self.assertEqual(block_to_block_type(text), expected)
        text = '- this is\n- not an\nunordered list'
        expected = 'paragraph'
        self.assertEqual(block_to_block_type(text), expected)
        text = '- this is also\n- not an\n-unordered list'
        expected = 'paragraph'
        self.assertEqual(block_to_block_type(text), expected)
        
    def test_ordered_list(self):
        text = '1. this is an\n2. ordered\n3. list'
        expected = 'ordered_list'
        self.assertEqual(block_to_block_type(text), expected)
        text = '1. this is\n2. not an\nunordered list'
        expected = 'paragraph'
        self.assertEqual(block_to_block_type(text), expected)
        text = '1. this is also\n2. not an\n3 unordered list'
        expected = 'paragraph'
        self.assertEqual(block_to_block_type(text), expected)
        text = '1. this is also also\n2. not an\n4. unordered list'
        expected = 'paragraph'
        self.assertEqual(block_to_block_type(text), expected)

if __name__ == "__main__":
    unittest.main()
