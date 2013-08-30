#!/usr/bin/python

import os
import subprocess

# define paths
vagrant_executable = '/usr/bin/vagrant'
script_path = os.path.realpath(__file__)
project_path = os.path.dirname(script_path)

# iterate over directories
def iterate_directory(path, parent_box_name, callback):
	for sub_name in os.listdir(path):
		sub_path = os.path.join(path, sub_name)
		if os.path.isdir(sub_path) and not sub_name.startswith('.'):
			box_name = sub_name if parent_box_name is None else '%s-%s' % (parent_box_name, sub_name)
			callback(sub_path, box_name, parent_box_name)
			iterate_directory(sub_path, box_name, callback)

def put_vagrantfile(path, box_name, parent_box_name):
	global project_path

	template_path = os.path.join(project_path, 'Vagrantfile-template')
	vagrantfile_path = os.path.join(path, 'Vagrantfile')
	box_url_path = os.path.join(path, 'box.url')

	box_url = file(box_url_path, 'r').read().splitlines()[0] if os.path.exists(box_url_path) else None

	template_file = file(template_path, 'r')
	template = template_file.read()

	vagrantfile = template % (parent_box_name if parent_box_name is not None else '%s-base' % box_name, box_url if box_url is not None else '')

	file(vagrantfile_path, 'w').write(vagrantfile)

def generate_box(path, box_name, parent_box_name):
	print '### Generating %s (%s)' % (box_name, path)

	# create vagrantfile
	put_vagrantfile(path, box_name, parent_box_name)

	# destroy vm if existing
	subprocess.call([vagrant_executable, 'destroy', '-f'], cwd=path)

	# create vm again
	subprocess.call([vagrant_executable, 'up'], cwd=path)

	# package vm into a box
	subprocess.call([vagrant_executable, 'package', '--output', '%s.box' % box_name], cwd=path)

	# install box
	subprocess.call([vagrant_executable, 'box', 'add', '-f', box_name, '%s.box' % box_name], cwd=path)

	# destroy vm
	subprocess.call([vagrant_executable, 'destroy', '-f'], cwd=path)

iterate_directory(project_path, None, generate_box)
