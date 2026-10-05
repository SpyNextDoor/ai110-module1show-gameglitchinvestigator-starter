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
| Resetting the game once the level of difficulty is changed. | - When you change the difficulty level, the game should reset to and the guess should fall within [low, high] boundaries for that level. | - Now, when you change difficulty level, the game doesn't change which doesn't make sense since each level have different guess attempts and different range for the secret number.       |                                                                                                                                                                                              |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

--> I used claude code

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

--> The biggest hurdle I encounted was being able to update the developer debugger info while as soon as I made a suggestion. I ended up commenting out the guess since you don't want a player to see the secret number before playing. But I wanted the player to be able to keep track of the attemps, and see their score. So I needed this part to update as we go. Claude suggest I use empty placeholders to reserve space for the panel since streamlit runs code top down.

```Python
info_slot = st.empty()
debug_slot = st.empty()
```

I tested this by running the game and seeing that the guess is saved as soon as it is submitted.

I had another issue where after each game, the placeholder of the guess did not clear itself. Claude suggested this code.

```Python
st.session_state[f"guess_input_{difficulty}"] = ""
```

I added this in the rest_game function and it worked.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

--> my code had a bug of casting the secret to a str when the remaning attempts are divisible by two. While generating test cases AI made a test case for this bug before I fixed it. When this test failed (str to str comparison) that's how I actually when back to fix it. There was a try/except clause in check guess that turned the guess also into a str so now the comparison was between strings not numbers. I ended up removing it.

```Python
def test_hint_with_string_secret_compares_numerically():
    # app.py passes the secret as a str on even attempts; 9 vs "10" must
    # still be "Too Low" (a string comparison would say "9" > "10").
    assert check_guess(9, "10")[0] == "Too Low"
    assert check_guess(100, "20")[0] == "Too High"
    assert check_guess(42, "42")[0] == "Win"
```

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

--> I ran the game again and then wrote tests later to fully confirm that the bug is fixed.

- Describe at least one test you ran (manual or using pytest)and what it showed you about your code.

```Python
def test_hint_with_string_secret_compares_numerically():
    # app.py passes the secret as a str on even attempts; 9 vs "10" must
    # still be "Too Low" (a string comparison would say "9" > "10").
    assert check_guess(9, "10")[0] == "Too Low"
    assert check_guess(100, "20")[0] == "Too High"
    assert check_guess(42, "42")[0] == "Win"
```

--> I ran this test via pytest. After converting the guess to a string the comparison failed. There was a try/except clause in check guess that turned the guess also into a str so now the comparison was between strings not numbers. This made me go back and fix this bug and removed the unnecessary string conversion.

- Did AI help you design or understand any tests? How?

--> It really helped because it generated the tests of things it helped me fix so it was able to explain the decisions it used to make those tests.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

--> streamlit is a package that renders python scripts. And what the reruns means is that is wipes the slate clean each time it runs. The code runs from top to bottom each time. So, whenever a user clicks a button, type anthing streamlit runs the entire app from top to bottom again.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

--> Commit as often as I can. That way I remember what the fix was and it helps me to have more meaningful commit messages.

--> Writing tests is equally important.

- What is one thing you would do differently next time you work with AI on a coding task?

--> I would halt on asking AI too soon and flex the thinking muscles a bit. Yes, AI helps identify bugs quicker but I think it is still necessary for the human to read through a code base, understand the logic and spot bugs.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

--> AI can't be trusted to do everything without a human checker to verify. Claude wrote a test for a bug I had in my code instead of suggesting to fix the bug.

--> AI needs clear instructions on what to do. The more clear, the better the answer.
