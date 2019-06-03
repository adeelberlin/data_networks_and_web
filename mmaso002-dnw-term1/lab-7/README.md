# Catflucks Application 

Here is a new improved version of catflucks.

It has the same functionality as the Lab 6 version, but more effort has
been made to separate concerns (i.e. to separate database interaction, logic and presentation).

**Noteworthy differences:**
+ The app configurables (i.e. installation specific variables) are now defined in config.py.
+ splash.py provides the main entry point to the app
+ A new template rendering function has been added to utils.py
+ The HTML is confined to .html files in the templates folder

*It is still not perfect!* There is much more we could do to improve portability/reusability...
Perhaps you can introduce further improvements to the **application design** in your own implementation?
