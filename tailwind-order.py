import sublime
import sublime_plugin
import json
import re


class TailwindOrderCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        file = sublime.load_resource(sublime.find_resources('data.json')[0])
        file = json.loads(file)
        dif = 0
        classes = self.view.find_all('(?<=class=")(.*?)(?=")')
        for item in classes:
            filters = {}
            item.a += dif
            item.b += dif
            region = item
            temp_classes = self.view.substr(item)
            temp_classes = re.sub(' +', ' ', temp_classes)
            temp_classes = temp_classes.split(' ')
            other_classes = temp_classes[:]
            sorted_class = ""
            for temp_class in temp_classes:
                for tw_class in file:
                    print(tw_class)
                    if temp_class.startswith(tw_class['name']):
                        print(temp_class)
                        if tw_class['kind'] in filters.keys() and temp_class not in filters[tw_class['kind']]:
                            print(filters[tw_class['kind']])
                            filters[tw_class['kind']].append(temp_class)
                            if temp_class in other_classes:
                                other_classes.remove(temp_class)
            for kind in filters.keys():
                filters[kind] = sorted(filters[kind])
                sorted_class += ' '.join(filters[kind])
                if filters[kind]:
                    sorted_class += ' '
            if other_classes:
                sorted_class += ' '.join(sorted(other_classes))
            self.view.replace(edit, region, sorted_class)
            dif += len(sorted_class) - len(str(self.view.substr(item)))

class CommandOnSave(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        view.run_command('tailwind_order')
