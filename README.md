# MkDocs Gen Nav Plugin

This plugin generates the `config['nav']` automatically for your MkDocs documentation site by finding all markdown files from the global `config['docs_dir']`.

## Rules

The following rules are used to generate the navigation:

* The file or directory names are used as the navigation title.
* If a path name starts with two digits and '_' characters, it is ignored in the title. This means that it is only used to sort the navigation list.
* If a path name starts with '_', it will be ignored. This means that the links to that markdown file should be a part of some other document manually.
* The file named "index.md" in the docs root dir will be ignored. (It will be used as Home page)

## Configuration

Add following lines to your `mkdocs.yml` configuration file:

```
plugins:
  - gen_nav:
      enabled: true
```

## Example

you can find example in [examples](./examples) directory

## Install

`pip install mkdocs-gen-nav-plugin`

## Development

[Development Guide](./docs/development.md)
