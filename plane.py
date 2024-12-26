class Plane:
    def __init__(self, name):
        self.name = name
        self.checklists =  self.checklists = {
            "pre-flight": [],
            "in-flight": [],
            "post-flight": []
        }

    def add_checklist(self, type, items):
        if type in self.checklists:
            self.checklists[type] = items
        else:
            print(f"Invalid type: {type}")
    
    def get_checklists(self, type):
        if type in self.checklists:
            return self.checklists[type]
        else:
            print(f"Checklist doesn't exist: {type}")
            print(f'Available types: {', '.join(self.checklists.keys())}')
            return None
