from copy import deepcopy
from pathlib import Path
import os
import shutil

from delimiter import markdown_to_html_node
from textnode import TextNode


def main():
	if os.path.exists('./public'):
		shutil.rmtree('./public')
	copy_dir('./static', './public')
	generate_pages_recursive("content","template.html","public")

def copy_dir(src, dest):
	if os.path.isfile(src):
		shutil.copy(src, dest)
	else:
		if os.path.exists(dest):
			shutil.rmtree(dest)
		os.mkdir(dest)
		sub_items = os.listdir(src)
		for item in sub_items:
			new_src = os.path.join(src, item)
			new_dest = os.path.join(dest, item)
			copy_dir(new_src, new_dest)

def extract_title(markdown):
	if not markdown.startswith('# '):
		raise Exception('Markdown has no h1 header')
	return markdown.split('\n', 1)[0].lstrip('# ')

def generate_page(from_path, template_path, dest_path):
	print(f'Generating page from {from_path} to {dest_path} using {template_path}')
	from_file = open(from_path)
	markdown = from_file.read()
	from_file.close()
	template_file = open(template_path)
	template = template_file.read()
	template_file.close()
	html_node = markdown_to_html_node(markdown)
	html_string = html_node.to_html()
	title = extract_title(markdown)
	template = template.replace('{{ Title }}', title)
	template = template.replace('{{ Content }}', html_string)
	if not os.path.exists(os.path.dirname(dest_path)):
		os.makedirs(os.path.dirname(dest_path))
	dest_file = open(dest_path, 'w+')
	dest_file.write(template)
	dest_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	template_file = open(template_path)
	template = template_file.read()
	template_file.close()
	for item in os.listdir(dir_path_content):
		item_path = os.path.join(dir_path_content, item)
		if os.path.isfile(item_path) and item_path.endswith('.md'):
			new_dest_path = os.path.join(dest_dir_path, item).removesuffix('.md') + '.html'
			print(f'Generating page from {item_path} to {new_dest_path} using {template_path}')
			from_file = open(item_path)
			markdown = from_file.read()
			from_file.close()

			html_node = markdown_to_html_node(markdown)
			html_string = html_node.to_html()
			title = extract_title(markdown)

			new_template = deepcopy(template)
			new_template = new_template.replace('{{ Title }}', title)
			new_template = new_template.replace('{{ Content }}', html_string)
			
			if not os.path.exists(os.path.dirname(new_dest_path)):
				os.makedirs(os.path.dirname(new_dest_path))
			new_dest_file = open(new_dest_path, 'w+')
			new_dest_file.write(new_template)
			new_dest_file.close()
		elif not os.path.isfile(item_path):
			new_dir_path_content = os.path.join(dir_path_content, item)
			new_dest_dir_path = os.path.join(dest_dir_path, item)
			generate_pages_recursive(new_dir_path_content, template_path, new_dest_dir_path)
	

main()
