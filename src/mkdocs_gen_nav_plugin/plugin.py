import os
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.config import config_options

log = get_plugin_logger(__name__)

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
        if file.endswith('_'):
            file = file[:-1]
        if file[0:2].isdigit() and file[2] == '_':
            file = file[3:]
        
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
        for file in files:
            file.dest_path = file.dest_uri = self.rename_item(file.dest_path)
            file.url = self.rename_item(file.url)
            file.abs_dest_path = self.rename_item(file.abs_dest_path)
        return files

    def create_nav_dict(self, base_dir, path, include):
        nav_dict = []
        for item in sorted(os.listdir(path)):
            item_path = os.path.join(path, item)
            item_title = os.path.splitext(item)[0]
            if item_title.startswith('_') or item_title == 'index':
                continue
            if item_title[0:2].isdigit() and item_title[2] == '_':
                item_title = item_title[3:]
            use_index = item_title.endswith('_')
            if use_index:
                item_title = item_title[:-1]
            if os.path.isfile(item_path) and item.endswith(include):
                nav_dict.append({self.format_title(item_title): os.path.relpath(item_path, base_dir)})
            elif use_index and os.path.isdir(item_path):
                log.info(item_path + ", marked as plugin source.")
                index_path = os.path.join(item_path, "index.md")
                if not os.path.exists(index_path):
                    raise Exception("index.md does not exist in: " + index_path)
                nav_dict.append({self.format_title(item_title): os.path.relpath(index_path, base_dir)})
            elif os.path.isdir(item_path):
                item_dict = self.create_nav_dict(base_dir, item_path, include)
                if item_dict:
                    nav_dict.append({self.format_title(item_title): item_dict})
        return nav_dict

    @staticmethod
    def format_title(title):
        formatted = " ".join([word.capitalize() for word in title.replace("-", " ").replace("_", " ").split()])
        return f'{formatted}'
