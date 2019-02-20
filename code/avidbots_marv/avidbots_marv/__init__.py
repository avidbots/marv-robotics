# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import yaml
import os

import marv
import marv_nodes
from marv_nodes.types_capnp import File
from marv_detail.types_capnp import Section, Widget

@marv.node(Section)
@marv.input('title', default='Reports')
@marv.input('dataset', marv_nodes.dataset)
def reports_section(dataset, title):
    """Create reports section

    Args:
        title (str): Title to be displayed for detail section.
        dataset: marv dataset

    Usage:
        - A folder is created with same name(without '.bag') and same parent folder as the bag file if this folder hasn't been created,
          a reports.yaml is created in this folder as well if this reports.yaml doesn't exist
        - We can mannually edit the reports.yaml to link more reports. After the reports.yaml is updated,
          marv server has to re-run reports_section node, 'marv run --force-deps --node avidbots_marv:reports_section --collection=bags'

    Returns
        One detail section.
    """

    # Create directory to store reports if it hasn't been created
    dataset = yield marv.pull(dataset)
    bag_paths = [x.path for x in dataset.files if x.path.endswith('.bag')]
    reports_dir = None
    if (len(bag_paths) < 1): raise RuntimeError('No bag path found in this dataset!')
    reports_dir = bag_paths[0].replace('.bag', '/')
    try:
        os.makedirs(reports_dir)
    except OSError:
        print('{} already exists!'.format(reports_dir))

    # Create reports.yaml to index any reports if is hasn't been created
    reports_yaml_path = '{}reports.yaml'.format(reports_dir)
    if not os.path.isfile(reports_yaml_path):
        reports_dict = {}
        reports_dict['bag file'] = bag_paths[0].replace('/scanroot', 'smb://172.16.0.10/nas/BagDatabase')
        reports_dict['reports.yaml'] = reports_yaml_path.replace('/scanroot', 'smb://172.16.0.10/nas/BagDatabase')
        with open(reports_yaml_path, 'w') as yaml_file:
            yaml.safe_dump(reports_dict, yaml_file, default_flow_style=False)
                                                                                
    # Load reports.yaml to show in Reports section
    reports_yaml = yaml.load(open('{}reports.yaml'.format(reports_dir)))
    widget_list = []
    # The bag file path and reports.yaml path are always listed first
    if reports_yaml['bag file']:
        widget_list.append({'title': 'bag file', 'link':{'href': reports_yaml['bag file'], 'title': reports_yaml['bag file']}})
    if reports_yaml['reports.yaml']:
        widget_list.append({'title': 'reports.yaml', 'link':{'href': reports_yaml['reports.yaml'], 'title': reports_yaml['reports.yaml']}})
    for key, value in reports_yaml.iteritems():
        if (key != 'bag file' and key != 'reports.yaml'):
            widget_list.append({'title': key, 'link':{'href': value, 'title': value}})
    section = {'title': title, 'widgets': widget_list}
    yield marv.push(section)
