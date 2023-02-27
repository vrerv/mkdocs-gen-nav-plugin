import os
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
        config['nav'] = nav_items
        return config

    def create_nav_dict(self, base_dir, path, include):
        nav_dict = []
        for item in sorted(os.listdir(path)):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path) and item.endswith(include):
                item_title = os.path.splitext(item)[0]
                if item_title.startswith('_') or item_title == 'index':
                    continue
                if item_title[0:2].isdigit() and item_title[2] == '_':
                    item_title = item_title[3:]
                nav_dict.append({self.format_title(item_title): os.path.relpath(item_path, base_dir)})
            elif os.path.isdir(item_path):
                item_dict = self.create_nav_dict(base_dir, item_path, include)
                if item_dict:
                    nav_dict.append({self.format_title(item): item_dict})
        return nav_dict

    @staticmethod
    def format_title(title):
        formatted = " ".join([word.capitalize() for word in title.replace("-", " ").replace("_", " ").split()])
        return f'{formatted}'
