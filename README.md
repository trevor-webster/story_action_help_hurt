A simple tkinter GUI for creating action sequences that represent a story, compliant with the json schema defined in action_sequence_schema.json.
Each action is carried out by one or more agents, and may affect one or more other characters. An action benefits characters on a scale from -1 to 1. If a character is not mentioned in othersAffected, the benefit of the action on that character is implied to be 0 (neutral net benefit).
Once all actions have been entered, the story actions can be saved by pressing "Save JSON", which will save the results in the story_actions_data directory.

ANNOTATION GUIDELINES
- The benefit or detriment of an action should be evaluated based primarily on the short-term impact of the action rather than the intent or long-term effects. Exceptions can be made to this, for example if a character sets a trap with intent to harm, this could be considered detrimental to their intended target.
- If a character advances their personal agenda, this can be considered to help them even if they receive no immediate benefit
- Emphasis should be on actions that move the plot forward, minor information exchanges can be conceptually grouped with the actions they inspire
- Order of events should generally follow the ordering at the level of discourse rather than story, i.e. the order they are described in the plot summary rather than the order they occur diagetically (in the world of the story). This is primarily for ease of annotation, to avoid having to untangle flashbacks etc.