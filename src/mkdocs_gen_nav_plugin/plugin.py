import os
import posixpath
from pathlib import Path

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options


class GenNavPlugin(BasePlugin):
    config_scheme = (
        ('nav_include', config_options.Type(str, default='.md')),
        ('enabled', config_options.Type(bool, default=True)),
    )

    def on_config(self, config, **kwargs):
        enabled = self.config['enabled']
        if not enabled:
            return
        docs_dir = config['docs_dir']
        nav_items = self.create_nav_dict(docs_dir, docs_dir, self.config['nav_include'])
        if isinstance(config['nav'], list):
            config['nav'].extend(nav_items)
        else:
            config['nav'] = nav_items
        return config

    def rename_item(self, path):
        file = os.path.basename(path)
        file = self.remove_prefix(file)

        parent_path = os.path.dirname(path)
        if parent_path != path:
            parent_path = self.rename_item(parent_path)
        else:
            if os.path.isabs(path):
                parent_path = os.path.dirname(path)
            else:
                parent_path = ""
        return os.path.join(parent_path, file)

    def on_files(self, files, config):
        """
        The files event is called after the files collection is populated from the
        docs_dir. Use this event to add, remove, or alter files in the collection. Note
        that Page objects have not yet been associated with the file objects in the
        collection. Use Page Events to manipulate page specific data.

        https://www.mkdocs.org/dev-guide/api/#mkdocs.structure.files.File
        :param files:
        :param config:
        :return:
        """
        for file in files:
            file.dest_path = self.rename_item(file.dest_path)
            file.dest_uri = Path(self.rename_item(file.dest_path)).as_posix()
            file.url = Path(self.rename_item(file.url)).as_posix()
            file.abs_dest_path = self.rename_item(file.abs_dest_path)
        return files

    def create_nav_dict(self, base_dir, path, include):
        nav_dict = []
        is_root = base_dir == path
        for item in self.list_files_to_process(path, include):
            item_path = posixpath.join(path, item)
            item_title = os.path.splitext(item)[0]
            if item_title.startswith('_') or (is_root and item_title == 'index'):
                continue
            item_title = self.remove_prefix(item_title)
            if os.path.isfile(item_path):
                nav_dict.append(
                    {self.format_title(item_title): posixpath.relpath(item_path, base_dir)})
            elif os.path.isdir(item_path):
                item_dict = self.create_nav_dict(base_dir, item_path, include)
                if item_dict:
                    nav_dict.append({self.format_title(item_title): item_dict})
        return nav_dict

    @staticmethod
    def list_files_to_process(path, include):
        return sorted(filter(
            lambda file: os.path.isdir(os.path.join(path, file)) or file.endswith(include)
            , os.listdir(path)
        ))

    @staticmethod
    def remove_prefix(item_title):
        if len(item_title) >= 3 and item_title[0:2].isdigit() and item_title[2] == '_':
            item_title = item_title[3:]
        return item_title

    @staticmethod
    def format_title(title):
        formatted = " ".join([word.capitalize() for word
                              in title.replace("-", " ").replace("_", " ").split()])
        return f'{formatted}'
