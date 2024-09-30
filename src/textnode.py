from htmlnode import LeafNode, ParentNode

class TextNode:
	text = None
	text_type = None
	url = None
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, node):
		return node.text == self.text and node.text_type == self.text_type and node.url == self.url

	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type}, {self.url})"
	
def text_node_to_html_node(text_node):
	match text_node.text_type:
		case 'text':
			return LeafNode(text_node.text, None, None)
		case 'bold':
			return LeafNode(text_node.text, "b", None)
		case 'italic':
			return LeafNode(text_node.text, "i", None)
		case 'code':
			return LeafNode(text_node.text, "code", None)
		case 'link':
			return LeafNode(text_node.text, "a", {'href': text_node.url})
		case 'image':
			return LeafNode('', "img", {'src': text_node.url, 'alt': text_node.text})
		case _:
			raise Exception()
