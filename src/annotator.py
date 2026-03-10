import tkinter as tk
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteEntry
import json
import os

class Annotator:
    def __init__(self):
        self.root = tk.Tk()
        self.annotator = tk.StringVar()
        self.title = tk.StringVar()
        self.rated_chars = tk.StringVar()
        self.actions = []
        self.agent_frames = []
        self.other_frames = []
        self.current_index = 0
        self.completion_values = []

    def launch_annotator(self):
        self.root.geometry('1200x800')
        self.root.title('Story Annotator v1.0')

        # Metadata fields
        self.annotator_label = tk.Label(self.root, text="Annotator Name:")
        self.annotator_entry = tk.Entry(self.root, textvariable=self.annotator)

        self.title_label = tk.Label(self.root, text="Story Title:")
        self.title_entry = tk.Entry(self.root, textvariable=self.title)

        self.text_label = tk.Label(self.root, text="Story Text (Wikipedia plot summary):")
        self.text_text = tk.Text(self.root, height=5)

        self.rated_label = tk.Label(self.root, text="Rated Characters (comma-separated):")
        self.rated_entry = tk.Entry(self.root, textvariable=self.rated_chars)

        self.submit_meta_btn = tk.Button(self.root, text="Submit Metadata", command=self.submit_metadata)

        # Grid metadata
        self.annotator_label.grid(row=0, column=0, sticky='w')
        self.annotator_entry.grid(row=0, column=1, columnspan=2, sticky='ew')
        self.title_label.grid(row=1, column=0, sticky='w')
        self.title_entry.grid(row=1, column=1, columnspan=2, sticky='ew')
        self.text_label.grid(row=2, column=0, sticky='w')
        self.text_text.grid(row=2, column=1, columnspan=2, sticky='ew')
        self.rated_label.grid(row=3, column=0, sticky='w')
        self.rated_entry.grid(row=3, column=1, columnspan=2, sticky='ew')
        self.submit_meta_btn.grid(row=4, column=1)

        self.annotator_entry.focus_set()
        self.root.mainloop()

    def submit_metadata(self):
        self.annotator_name = self.annotator.get().strip()
        self.story_title = self.title.get().strip()
        self.story_text = self.text_text.get("1.0", tk.END).strip()
        self.rated_characters = [c.strip() for c in self.rated_chars.get().split(',') if c.strip()]
        self.completion_values.extend(self.rated_characters)

        if not self.annotator_name or not self.story_title or not self.story_text:
            messagebox.showerror("Error", "Annotator name, story title, and story text are required.")
            return

        # Hide metadata widgets
        widgets_to_hide = [
            self.annotator_label, self.annotator_entry, self.title_label, self.title_entry,
            self.text_label, self.text_text, self.rated_label, self.rated_entry, self.submit_meta_btn
        ]
        for w in widgets_to_hide:
            w.grid_remove()

        # Show action form
        self.show_action_form()

    def show_action_form(self):
        self.desc_label = tk.Label(self.root, text="Action Description:")
        self.desc_entry = tk.Entry(self.root)

        self.action_label = tk.Label(self.root, text="Action Verb:")
        self.action_entry = tk.Entry(self.root)

        self.agents_label = tk.Label(self.root, text="Agents:")
        self.add_agent_btn = tk.Button(self.root, text="Add Agent", command=self.add_agent)
        self.agents_frame = tk.Frame(self.root)

        self.others_label = tk.Label(self.root, text="Others Affected:")
        self.add_other_btn = tk.Button(self.root, text="Add Affected", command=self.add_other)
        self.others_frame = tk.Frame(self.root)

        self.prev_btn = tk.Button(self.root, text="Previous Action", command=self.prev_action, state=tk.DISABLED)
        self.next_btn = tk.Button(self.root, text="Next Action", command=self.next_action, state=tk.NORMAL)
        self.save_btn = tk.Button(self.root, text="Save JSON", command=self.save_json)

        # Grid action form
        self.desc_label.grid(row=0, column=0, sticky='w')
        self.desc_entry.grid(row=0, column=1, columnspan=2, sticky='ew')
        self.action_label.grid(row=1, column=0, sticky='w')
        self.action_entry.grid(row=1, column=1, columnspan=2, sticky='ew')
        self.agents_label.grid(row=2, column=0, sticky='w')
        self.add_agent_btn.grid(row=2, column=1)
        self.agents_frame.grid(row=3, column=0, columnspan=4, sticky='ew')
        self.others_label.grid(row=4, column=0, sticky='w')
        self.add_other_btn.grid(row=4, column=1)
        self.others_frame.grid(row=5, column=0, columnspan=4, sticky='ew')
        self.prev_btn.grid(row=0, column=3)
        self.next_btn.grid(row=1, column=3)
        self.save_btn.grid(row=6, column=3)

        new_action = {'description': '', 'action': '', 'agents': [{'name': '', 'benefit': ''}], 'othersAffected': []}
        self.actions.append(new_action)
        self.load_action(self.current_index)

    def add_agent(self):
        self._add_person_frame(self.agents_frame, self.agent_frames)

    def add_other(self):
        self._add_person_frame(self.others_frame, self.other_frames)

    def _add_person_frame(self, parent_frame, frames_list):
        frame = tk.Frame(parent_frame)
        name_label = tk.Label(frame, text="Name:")
        name_entry = AutocompleteEntry(frame, completevalues=self.completion_values)
        benefit_label = tk.Label(frame, text="Benefit (-1 to 1):")
        benefit_entry = tk.Entry(frame)
        remove_btn = tk.Button(frame, text="Remove", command=lambda: self.remove_frame(frame, frames_list))

        name_label.grid(row=0, column=0)
        name_entry.grid(row=0, column=1)
        benefit_label.grid(row=0, column=2)
        benefit_entry.grid(row=0, column=3)
        remove_btn.grid(row=0, column=4)

        frame.pack(fill='x')
        frames_list.append({'frame': frame, 'name': name_entry, 'benefit': benefit_entry})

    def remove_frame(self, frame, frames_list):
        for f in frames_list:
            if f['frame'] == frame:
                f['frame'].destroy()
                frames_list.remove(f)
                break

    def is_current_action_empty(self):
        desc = self.desc_entry.get().strip()
        if len(desc) > 0:
            return False

        act = self.action_entry.get().strip()
        if len(act) > 0:
            return False

        agents = self._collect_persons(self.agent_frames)
        if agents is not None:
            if len(agents) > 1:
                return False
            # if there's only one agent, check if it's the default empty one
            if len(agents) == 1 and (len(agents[0]['name']) > 0 or len(agents[0]['benefit']) > 0):
                return False

        others = self._collect_persons(self.other_frames)
        if others is not None and len(others) > 0:
            return False
        
        return True


    def save_current_action(self):
        desc = self.desc_entry.get().strip()
        act = self.action_entry.get().strip()

        agents = self._collect_persons(self.agent_frames)
        if agents is None:
            return False

        others = self._collect_persons(self.other_frames)

        if not desc or not act or not agents:
            messagebox.showerror("Error", "Description, action verb, and at least one agent are required.")
            return False

        self.actions[self.current_index] = {
            'description': desc,
            'action': act,
            'agents': agents,
            'othersAffected': others
        }
        
        for agent in agents:
            if agent['name'] not in self.completion_values:
                self.completion_values.append(agent['name'])
        if others is not None:
            for other in others:
                if other['name'] not in self.completion_values:
                    self.completion_values.append(other['name'])
        return True

    def load_action(self, index):
        action = self.actions[index]
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, action['description'])
        self.action_entry.delete(0, tk.END)
        self.action_entry.insert(0, action['action'])

        # Clear existing frames
        for f in self.agent_frames + self.other_frames:
            f['frame'].destroy()
        self.agent_frames = []
        self.other_frames = []

        # Add frames for agents
        for agent in action['agents']:
            self._add_person_frame(self.agents_frame, self.agent_frames)
            last = self.agent_frames[-1]
            last['name'].insert(0, agent['name'])
            last['benefit'].insert(0, str(agent['benefit']))

        # Add frames for others
        for other in action['othersAffected']:
            self._add_person_frame(self.others_frame, self.other_frames)
            last = self.other_frames[-1]
            last['name'].insert(0, other['name'])
            last['benefit'].insert(0, str(other['benefit']))

        self.desc_entry.focus_set()

    def prev_action(self):
        if self.current_index == len(self.actions) - 1 and self.is_current_action_empty():
            self.actions.pop()
        elif not self.save_current_action():
            return
        self.current_index -= 1
        self.load_action(self.current_index)
        self.update_buttons()

    def next_action(self):
        if not self.save_current_action():
            return
        
        self.current_index += 1
        if self.current_index == len(self.actions):
            # Add new action
            new_action = {'description': '', 'action': '', 'agents': [{'name': '', 'benefit': ''}], 'othersAffected': []}
            self.actions.append(new_action)

        self.load_action(self.current_index)
        self.update_buttons()

    def update_buttons(self):
        self.prev_btn.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)

    def _collect_persons(self, frames_list):
        persons = []
        for f in frames_list:
            name = f['name'].get().strip()
            benefit_str = f['benefit'].get().strip()
            if not name and not benefit_str:
                continue
            if not name:
                messagebox.showerror("Error", "Name and benefit are required for all persons.")
                return None
            try:
                benefit = float(benefit_str)
                if not -1 <= benefit <= 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Benefit must be a number between -1 and 1.")
                return None
            persons.append({'name': name, 'benefit': benefit})
        return persons

    def save_json(self):
        if not self.actions:
            messagebox.showerror("Error", "At least one action is required.")
            return

        data = {
            'metadata': {
                'title': self.story_title,
                'text': self.story_text,
                'ratedCharacters': self.rated_characters,
                'annotator': self.annotator_name
            },
            'actions': self.actions
        }

        filename = f"{self.story_title.replace(' ', '_').lower()}_actions.json"
        filepath = os.path.join('story_actions_data', filename)

        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Saved", f"Data saved to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")