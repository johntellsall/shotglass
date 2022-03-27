# Motivation

## Ask HN: How do you search large codebases before adding a feature or fixing bug?

 https://news.ycombinator.com/item?id=30819579

### Why / Steps

Why do we need to search source-code?
  1. Quickly learn the domain and context of the application
  2. After adding a feature, we should aware if we broke anything (assume you work with code that doesn't have test-case), it helps even to search testcases
  3. Find similar code and ensure you are improving quality of the overall similar code (not just fixing current bug)
  4. Understand how application behaves when there are production issues.

Below is my steps.

  1. Read the relevant code, and know certain domain keyword, variable names (inclusive class/method/function)
  2. Use the bitbucket/GitHub/git search
  3. Use the grep
  4. Use the git-grep

### Other Tools

* OpenGrok
