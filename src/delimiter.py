import re
from textnode import TextNode, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

def text_to_textnodes(text):
    node = TextNode(text, 'text', None)
    nodes = split_nodes_delimiter([node], '**', 'bold')
    nodes = split_nodes_delimiter(nodes, '*', 'italic')
    nodes = split_nodes_delimiter(nodes, '`', 'code')
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    valid_types = ['text', 'bold','italic','code','link','image']
    if text_type not in valid_types:
        raise Exception("Specified text_type not valid")
    for node in old_nodes:
        if node.text_type == 'text':
            regular_type = node.text_type
            current_type = node.text_type
            if node.text.count(delimiter) % 2 != 0:
                raise Exception(f'No closing delimiter found ({delimiter})')
            node_strings = node.text.split(delimiter)
            if len(node_strings) == 1:
                new_nodes.append(node)
                continue
            for string in node_strings:
                new_node = TextNode(string, current_type)
                new_nodes.append(new_node)
                if current_type == regular_type:
                    current_type = text_type
                else:
                    current_type = regular_type
        elif node.text_type not in valid_types:
            raise Exception("Node type not valid")
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    text_type_image = 'image'
    text_type_text = 'text'
    for node in old_nodes:
        if node.text_type == text_type_text:
            current_text = node.text
            images = extract_markdown_images(node.text)
            for image in images:
                sections = current_text.split(f"![{image[0]}]({image[1]})", 1)
                if sections[0] != '':
                    new_nodes.append(TextNode(sections[0], text_type_text))
                new_nodes.append(TextNode(image[0], text_type_image, image[1]))
                current_text = sections[1].removeprefix(f"![{image[0]}]({image[1]})")
            if current_text != '':
                new_node = TextNode(current_text, text_type_text)
                new_nodes.append(new_node)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    text_type_link = 'link'
    text_type_text = 'text'
    for node in old_nodes:
        if node.text_type == text_type_text:
            current_text = node.text
            links = extract_markdown_links(node.text)
            for link in links:
                sections = current_text.split(f"[{link[0]}]({link[1]})", 1)
                if sections[0] != '':
                    new_nodes.append(TextNode(sections[0], text_type_text))
                new_nodes.append(TextNode(link[0], text_type_link, link[1]))
                current_text = sections[1].removeprefix(f"[{link[0]}]({link[1]})")
            if current_text != '':
                new_nodes.append(TextNode(current_text, text_type_text))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    format_matches = []
    for match in matches:
        alt_text = match[0].replace('[', '').replace(']', '')
        url = match[1].replace('(', '').replace(')', '')
        format_match = (alt_text, url)
        format_matches.append(format_match)
    return format_matches

def extract_markdown_links(text):
    regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    format_matches = []
    for match in matches:
        alt_text = match[0].replace('[', '').replace(']', '')
        url = match[1].replace('(', '').replace(')', '')
        format_match = (alt_text, url)
        format_matches.append(format_match)
    return format_matches

def markdown_to_blocks(markdown):
    lines = markdown.split('\n\n')
    out_lines = []
    for line in lines:
        line = line.lstrip().rstrip()
        if line != '':
            out_lines.append(line.lstrip().rstrip())
    return(out_lines)

def block_to_block_type(block):
    if block.startswith('#'):
        counter = 0
        for char in block:
            if char == '#':
                counter += 1
            elif char == ' ':
                return 'heading'
            else:
                return 'paragraph'
            if counter > 6:
                return 'paragraph'
        return 'heading'
    elif block.startswith('```') and block.endswith('```'):
        return 'code'
    elif block.startswith('>'):
        lines = block.split('\n')
        for line in lines:
            if not line.startswith('>'):
                return 'paragraph'
        return 'quote'
    elif block.startswith('* '):
        lines = block.split('\n')
        for line in lines:
            if not line.startswith('* '):
                return 'paragraph'
        return 'unordered_list'
    elif block.startswith('- '):
        lines = block.split('\n')
        for line in lines:
            if not line.startswith('- '):
                return 'paragraph'
        return 'unordered_list'
    elif block.startswith('1. '):
        lines = block.split('\n')
        counter = 1
        for line in lines:
            if not line.startswith(f'{counter}. '):
                return 'paragraph'
            counter += 1
        return 'ordered_list'
    else:
        return 'paragraph'
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_children = text_to_children(block, block_type)
        block_node = block_to_parent(block_type, block_children)
        if block_type == 'heading':
            block_node.children[0].value = block_node.children[0].value.lstrip('#').lstrip(' ')
        children.append(block_node)
    parent_node = ParentNode(children, 'div')
    return parent_node

def text_to_children(block, block_type):
    match block_type:
        case 'heading':
            text_nodes = text_to_textnodes(block)
            return [text_node_to_html_node(node) for node in text_nodes]
        case 'code':
            block = block.lstrip('```')
            block = block.rstrip('```')
            text_nodes = text_to_textnodes(block)
            node_list = [text_node_to_html_node(node) for node in text_nodes]
            code_node = ParentNode(node_list, 'code', None)
            return [code_node]
        case 'quote':
            block = block.replace('> ', '')
            text_nodes = text_to_textnodes(block)
            return [text_node_to_html_node(node) for node in text_nodes]
        case 'unordered_list':
            html_nodes = []
            lines = block.split('\n')
            for line in lines:
                if line == '':
                    continue
                if line[0] == '-':
                    line = line.removeprefix('- ')
                if line[0] == '*':
                    line = line.removeprefix('* ')
                text_nodes = text_to_textnodes(line)
                html_nodes.append(ParentNode([text_node_to_html_node(node) for node in text_nodes], 'li'))
            return html_nodes
        case 'ordered_list':
            html_nodes = []
            lines = block.split('\n')
            counter = 1
            for line in lines:
                line = line.lstrip(f'{counter}. ')
                counter += 1
                text_nodes = text_to_textnodes(line)
                html_nodes.append(ParentNode([text_node_to_html_node(node) for node in text_nodes], 'li'))
            return html_nodes
        case 'paragraph':
            text_nodes = text_to_textnodes(block)
            return [text_node_to_html_node(node) for node in text_nodes]
        case _:
            raise Exception('text_to_children received invalid block type')
    
def block_to_parent(block_type, children):
    match block_type:
        case 'heading':
            h_number = heading_counter(children[0].value)
            return ParentNode(children, f'h{h_number}', None)
        case 'code':
            return ParentNode(children, 'pre', None)
        case 'quote':
            return ParentNode(children, 'blockquote', None)
        case 'unordered_list':
            return ParentNode(children, 'ul', None)
        case 'ordered_list':
            return ParentNode(children, 'ol', None)
        case 'paragraph':
            return ParentNode(children, 'p', None)
        case _:
            raise Exception("Block type not found")

def heading_counter(heading):
    counter = 0
    for char in heading:
        if char == '#':
            counter += 1
        elif char == ' ':
            return counter
        else:
            return 0
    return counter