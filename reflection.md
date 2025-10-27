*Name: Nikita*  
*SRN: PES2UG23CS387* 
*LAB 5* 

**REFLECTION QUESTIONS:**

**1.	Which issues were the easiest to fix, and which were the hardest? Why?**  
The style issues were the easiest to fix because they required simple changes. 
-Trailing whitespace: Simply delete spaces at line ends 
-Function naming (snake_case): Straightforward find-and-replace renaming 
-Missing blank lines: Add two blank lines between functions  
-Missing docstrings: Template-based addition of documentation strings 
Hardest Issues
The logic and security issues required careful refactoring:​ 
-Mutable default argument (logs=[]): Required understanding Python's object initialization behavior and how default arguments persist across function calls​ 
-Bare except with pass: Needed analysis of what exceptions could occur, then implementing specific exception handling with proper error reporting​ 
-Input validation: Required comprehensive type checking logic for each parameter across multiple functions, adding 30+ lines of validation code​ 
-Logging configuration: Balancing between f-strings for readability and lazy % formatting for performance optimization in logging calls 

**2.	Did the static analysis tools report any false positives? If so, describe one example.** 
Yes, I think the global statement warning is mostly a false positive in this context. Pylint flags all global statements as warnings because they're generally considered poor practice in large applications. However, for this simple inventory script, using a global stock_data dictionary is a reasonable design choice.

**3.	How would you integrate static analysis tools into your actual software development workflow? Consider continuous integration (CI) or local development practices.** 
   
For Local development:

-Run Flake8 and Bandit automatically before each commit to catch issues immediately 
-IDE integration: Configure VSCode/PyCharm to run Pylint on save, providing real-time feedback  
-Local scripts: Create a lint.sh script that runs all three tools sequentially before pushing code 

For CI pipeline: 
Github action example: 
name: Run Static Analysis 
  run: | 
    flake8 . --max-line-length=100 
    pylint **/*.py --fail-under=8.0 
    bandit -r . -ll 


**4.	What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?** 
   
SECURITY: 
-Enhanced error handling with specific exception types instead of silent failures, preventing crash scenarios 
-Added input validation protecting against type confusion bugs and invalid data processing 

READABILITY: 
-Function names now follow Python conventions (add_item vs addItem), making code immediately recognizable to Python developers 
-Comprehensive docstrings provide inline documentation with argument types and return values 
-Consistent formatting with proper spacing makes the code readable 

MAINTAINABILITY: 
Logging infrastructure enables debugging in production without adding print statements 
