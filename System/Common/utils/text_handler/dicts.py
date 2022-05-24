# -*- encoding: utf-8 -*-
"""
@File Name      :   dicts.py    
@Create Time    :   2022/3/2 19:37
@Description    :   
@Version        :   
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

from copy import deepcopy


def dict_level_order_traversal(raw_dict: dict) -> list:
    """
    字典的层次遍历，并在第一个节点（即根节点）构建树形结构
    技巧：深度优先用递归，广度优先用队列。
    :param raw_dict:可嵌套字典的字典对象
    :return:节点列表，每个节点含有此节点下面的树形结构和原字典结构信息，整个列表的顺序是树的构建顺序
    """
    order = []
    temp_order = [{'id': 0, 'name': 'root', 'label': 'root', 'dict_children': raw_dict, 'parent_id': -1}]
    count = 0
    while temp_order:
        item = temp_order.pop(0)
        if isinstance(item['dict_children'], dict):
            item['children'] = []
            for key, value in item['dict_children'].items():
                count += 1
                node = {'id': count, 'name': key, 'label': key, 'dict_children': value, 'parent_id': item['id']}
                temp_order.append(node)
                item['children'].append(node)
        order.append(item)
    return order


def recursion_to_tree(raw_tree: list[dict]) -> list[dict]:
    """
    递归构建树形结构
    :param raw_tree:
    :return:
    """
    for node in raw_tree:
        node.pop('name')
        node.pop('parent_id')
        if node.get('children', []):
            node.pop('dict_children')
            recursion_to_tree(node['children'])
        else:
            node['value'] = node.pop('dict_children')
    return raw_tree


def filter_tree_from_level_order_traversal(order: list) -> list:
    """
    根据层次遍历的结果，过滤掉不需要的节点
    :param order:层次遍历的结果
    :return:过滤后的节点列表
    """
    root = [deepcopy(order[0])]
    return recursion_to_tree(root)[0]['children']


def dict_to_tree(raw_dict: dict):
    """
    上面过程的总和
    :param raw_dict:
    :return:
    """
    return filter_tree_from_level_order_traversal(dict_level_order_traversal(raw_dict))


def get_tree_ids(tree: list) -> dict:
    ids = {}
    temp_nodes = [node for node in tree]
    while temp_nodes:
        node = temp_nodes.pop(0)
        if node.get('children', []):
            for child in node['children']:
                temp_nodes.append(child)
        else:
            ids[node['id']] = node['value']
    return ids
