#! /usr/bin/env python

from __future__ import print_function

import markdown2
import pystache
import pystache.parser
import json
import re
import types

import schlub.util


class Builder(object):
    def __init__(self, config=None):
        self.items = {}
        self.templates = {}

        self.config = None
        if config:
            with open(config) as f:
                self.config = json.load(f)
                    
            

    def build(self):
        self.readTemplates()
        self.readItems()


        for name, item in self.items.items():
            rendered = item.content()

            fileName = "site/{}.html".format(name)
            schlub.util.writeWithCreate(fileName, rendered)

    def readItems(self):
        itemFiles = schlub.util.findFiles("items", "*.json")

        for itemFile in itemFiles:
            name = schlub.util.fileNameToKey(itemFile)
            self.items[name] = Item(itemFile, self.items, self.templates,
                                    self.config)

    def readTemplates(self):
        templateFiles = schlub.util.findFiles("templates", "*.json")

        for templateFile in templateFiles:
            name = schlub.util.fileNameToKey(templateFile)
            self.templates[name] = Template(templateFile)

        for template in self.templates.values():
            template.doNesting(self.templates)

class Item(object):
    rendering = None
    def __init__(self, fileName, items, templates, config=None):
        try:
            self.itemView = items.viewvalues() # Python 2
        except AttributeError:
            self.itemView = items.values() # Python 3
        self.templates = templates
        self.rendering = False

        self.filterAttribute = "tags"

        if config:
            self.__dict__.update(config)

        with open(fileName) as f:
            try:
                item = self.read(f)
            except Exception as error:
                print("Could not read item", fileName)
                print(error)
                raise

            if "content" in item:
                item["_content"] = item["content"]
                del item["content"]

            self.__dict__.update(item)

            self.parseContent()

    def read(self, f):
        item = json.load(f)
        return item

    def parseContent(self): 
        if hasattr(self, "markdown"):
            with open("markdown/{}.markdown".format(self.markdown)) as f:
                self._content = markdown2.markdown(f.read())

    def content(self):
        if self.rendering:
            if hasattr(self, "_content"):
                return pystache.render(self._content, self)
            return ""
        self.rendering = True
        self.processItems()
        content = self.templates[self.template].render(self)
        self.rendering = False
        return content

    def processItems(self):
        self.items = list(self.itemView)
        if hasattr(self, "filter"):
            self.items = [item for item in self.items
                          if item.has(self.filter, self.filterAttribute)]

        if hasattr(self, "sort"):
            self.items.sort(key=lambda x: x.sortKey(self.sort))

    def has(self, filter, attributeName):
        if not hasattr(self, attributeName):
            return False
        attribute = self.__dict__[attributeName]
        if isinstance(attribute, types.ListType):
            return filter in attribute
        else:
            return attribute == filter

    def sortKey(self, parameter):
        if hasattr(self, parameter):
            return False, self.__dict__[parameter]
        return True, None
            

class Template(object):
    def __init__(self, fileName):
        with open(fileName) as f:
            try:
                template = self.read(f) 
            except Exception as error:
                print("Could not read template:", fileName)
                print(error)
                raise

            self.__dict__.update(template)

            self.parseContent()

    def read(self, f):
        template = json.load(f)

        if not "mustache" in template:
            raise KeyError("Template contains no content")
        return template

    def parseContent(self):
        with open("mustache/{}.mustache".format(self.mustache)) as f:
            self.content = f.read()

    def doNesting(self, templates):
        if hasattr(self, "parent"):
            parent = templates[self.parent]
            parent.doNesting(templates)
#            self.content = parent.render({"content": self.content})
            self.content = re.sub("{{{\s*content\s*}}}", self.content,
                                  parent.content)
            self.parent = None
        return self.content
            

    def render(self, item):
        try:
            #print("Rendering", self.content, "with", item)
            content = self.content
            return pystache.render(content, item)
        except pystache.parser.ParsingError as error:
            print("Could not parse template: {}.mustache".format(self.mustache))
            print(error)
            raise

