# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input                                                       | Expected Behavior                                                                                                                        | Actual Behavior                                                                                                                                                                             | Console Output / Error                                                                                                                                                                       |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hint is off                                                 | - When you make a guess > actual_number hint should tell you to**go lower** or **go higher** when guess < actual_number    | hint just tells you randomly what direction to go to.                                                                                                                                       | There was no error. The output was just wrong because the logic was reversed.                                                                                                                |
| new_game button does not reset the game                     | - When you press "New Game" the game should reset and you start another round                                                            | nothing happens when you press "New Game".                                                                                                                                                  | <br /><module></module>                                                                                                                                                                      |
| Updating the developer debug info on submit                 | - When you press submit to submit a guess, the developer panel should update immediately without waiting for the next guess              | - now the developer debug panel updates guess i after guess i+1 is submitted. So, if the guess is correct it does not display that the game is won i.e session state does not update to won | AttributeError: st.session_state has no attribute "status". Did you forget to initialize it? More info: https://docs.streamlit.io/develop/concepts/architecture/session-state#initialization |
| Resetting the game once the level of difficulty is changed. | - When you change the difficulty level, the game should reset to and the guess should fall within [low, high] boundaries for that level. | -                                                                                                                                                                                           |                                                                                                                                                                                              |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
