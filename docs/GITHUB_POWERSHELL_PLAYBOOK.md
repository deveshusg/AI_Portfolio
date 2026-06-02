# GITHUB POWERSHELL PLAYBOOK

## A Practical Git & GitHub Guide for VS Code Users

---

# SECTION 1: WHAT IS GIT?

## What do I want to know?

What exactly is Git and why do developers use it?

---

## Simple Answer

Git is a time machine for your code.

Imagine you are writing a book.

Every time you finish a chapter, you save a snapshot.

Later, if you make a mistake, you can go back to any previous snapshot.

Git does exactly that for code.

---

## Without Git

```text
Project
│
├── app.py
├── app_final.py
├── app_final_v2.py
├── app_final_v3.py
├── app_final_really_final.py
└── app_final_final_final.py
```

This becomes impossible to manage.

---

## With Git

```text
Project
│
├── app.py
│
└── History
    ├── Version 1
    ├── Version 2
    ├── Version 3
    └── Version 4
```

Every version is stored automatically.

---

## What Problems Does Git Solve?

### Problem 1

You broke something.

Git lets you go back.

---

### Problem 2

You want to experiment.

Git lets you create branches.

---

### Problem 3

You want backups.

GitHub stores your repository online.

---

### Problem 4

You want to see what changed.

Git tracks every modification.

---

# SECTION 2: WHAT IS GITHUB?

## What do I want to know?

What is the difference between Git and GitHub?

---

## Git

Git lives on your computer.

Example:

```text
C:\Users\deves\OneDrive\Documents\Local AI
```

Git tracks changes locally.

---

## GitHub

GitHub lives online.

Example:

```text
https://github.com/deveshusg/AI_Portfolio
```

GitHub stores your repository on the internet.

---

## Simple Analogy

### Git

```text
Microsoft Word
```

### GitHub

```text
OneDrive
```

Git manages versions.

GitHub stores those versions online.

---

## Can Git Exist Without GitHub?

Yes.

You can use Git forever without GitHub.

---

## Can GitHub Exist Without Git?

No.

GitHub is built around Git.

---

# SECTION 3: THE FOUR GIT AREAS

This is the most important concept in Git.

If you understand this, Git becomes easy.

---

## Area 1: Working Directory

This is where you edit files.

Example:

```text
README.md
app.py
requirements.txt
```

You are actively changing files here.

---

## Area 2: Staging Area

Git's waiting room.

You tell Git:

```text
I want these changes included in my next commit.
```

Example:

```powershell
git add README.md
```

README.md moves into the staging area.

---

## Area 3: Local Repository

Git saves a snapshot.

Example:

```powershell
git commit -m "Update README"
```

Git creates a permanent checkpoint.

---

## Area 4: Remote Repository

GitHub.

Example:

```powershell
git push
```

Your commits are uploaded.

---

## Visual Diagram

```text
WORKING DIRECTORY
        │
        │ git add
        ▼
STAGING AREA
        │
        │ git commit
        ▼
LOCAL REPOSITORY
        │
        │ git push
        ▼
GITHUB
```

---

# SECTION 4: THE DAILY GIT WORKFLOW

This is the workflow you will use 95% of the time.

---

## Step 1

Make changes.

Example:

```text
Edit README.md
Create app.py
Update requirements.txt
```

---

## Step 2

Check status.

```powershell
git status
```

---

## Step 3

Stage files.

```powershell
git add .
```

or

```powershell
git add README.md
```

---

## Step 4

Commit changes.

```powershell
git commit -m "Add PDF upload feature"
```

---

## Step 5

Push to GitHub.

```powershell
git push
```

---

## Daily Workflow Diagram

```text
Change Files
      │
      ▼
git status
      │
      ▼
git add .
      │
      ▼
git commit
      │
      ▼
git push
```

---

# SECTION 5: THE MOST IMPORTANT COMMAND

If you forget everything else, remember this:

```powershell
git status
```

---

## What does it do?

Shows Git's current situation.

Think of it as:

```text
"Tell me what is going on."
```

---

## Example 1

```powershell
git status
```

Output:

```text
On branch develop

nothing to commit, working tree clean
```

Meaning:

```text
Everything is saved.
Everything is committed.
Nothing is wrong.
```

---

## Example 2

Output:

```text
modified: README.md
```

Meaning:

```text
README.md changed.
Git sees it.
Git has NOT committed it yet.
```

---

## Next Step

```powershell
git add README.md
```

---

## Example 3

Output:

```text
Untracked files:
    app.py
```

Meaning:

```text
Git found a new file.

Git is not tracking it yet.
```

---

## Fix

```powershell
git add app.py
```

---

## Rule

Whenever confused, run:

```powershell
git status
```

This should become muscle memory.

---

# SECTION 6: YOUR AI_PORTFOLIO WORKFLOW

For this repository specifically.

---

## Starting Work

Switch to the development branch:

```powershell
git checkout develop
```

Verify:

```powershell
git branch
```

Expected:

```text
* develop
  main
```

---

## While Working

Check status:

```powershell
git status
```

Stage changes:

```powershell
git add .
```

Create a commit:

```powershell
git commit -m "Meaningful description"
```

Push to GitHub:

```powershell
git push
```

---

## Project Complete

Switch to main:

```powershell
git checkout main
```

Merge develop:

```powershell
git merge develop
```

Push:

```powershell
git push
```

---

## Golden Rule

```text
Work on develop.

Keep main stable.
```

---

# PART 1 SUMMARY

You learned:

- What Git is
- What GitHub is
- The Four Git Areas
- The Daily Workflow
- The Importance of `git status`
- The AI_Portfolio Branch Strategy

---

# QUICK REFERENCE

## Check Status

```powershell
git status
```

## See Branches

```powershell
git branch
```

## Switch Branch

```powershell
git checkout develop
```

## Stage Everything

```powershell
git add .
```

## Commit

```powershell
git commit -m "Your message"
```

## Push

```powershell
git push
```

## Pull

```powershell
git pull
```

## Merge Develop into Main

```powershell
git checkout main
git merge develop
git push
```

---

# PART 2 - DAILY GIT COMMANDS

In Part 1, we learned:

- What Git is
- What GitHub is
- The Four Git Areas
- The Daily Workflow

In Part 2, we will learn the commands you will use every day.

---

# SECTION 7: STAGING FILES (`git add`)

## What do I want to do?

I changed files.

I want Git to include those changes in my next commit.

---

## Command

```powershell
git add filename
```

Example:

```powershell
git add README.md
```

---

## What does it do?

Moves the file from:

```text
Working Directory
```

to:

```text
Staging Area
```

---

## Visual Example

Before:

```text
README.md
    ↓
Modified
```

After:

```powershell
git add README.md
```

```text
README.md
    ↓
Staged
```

---

## Add Everything

Most common command:

```powershell
git add .
```

Meaning:

```text
Add all changes in the current folder and subfolders.
```

---

## Verify

```powershell
git status
```

Example:

```text
Changes to be committed:

    modified: README.md
```

Meaning:

```text
Git is ready to commit README.md
```

---

## Common Mistake

You run:

```powershell
git commit -m "Update README"
```

and nothing happens.

Reason:

```text
You forgot git add
```

Fix:

```powershell
git add README.md
git commit -m "Update README"
```

---

# SECTION 8: COMMITTING CHANGES (`git commit`)

## What do I want to do?

Create a checkpoint.

---

## Command

```powershell
git commit -m "Your message"
```

Example:

```powershell
git commit -m "Add PDF upload feature"
```

---

## What does it do?

Creates a snapshot.

Think:

```text
Save Game
```

for your project.

---

## Good Commit Messages

Good:

```text
Add PDF upload feature

Fix memory summarization bug

Create embeddings module

Update README documentation
```

Bad:

```text
Update

Stuff

Changes

asdf
```

---

## Verify

```powershell
git log --oneline
```

Example:

```text
7c3ab21 Add PDF upload feature
2f36ad8 Replace basic README
```

---

# SECTION 9: VIEWING HISTORY (`git log`)

## What do I want to do?

See previous commits.

---

## Command

```powershell
git log
```

---

## Easier Version

```powershell
git log --oneline
```

Example:

```text
2f36ad8 Replace basic README
3d6c7e4 Update README
b39a03f Project 03 complete
```

---

## Visual Version

Best version:

```powershell
git log --oneline --graph --decorate --all
```

Example:

```text
* 2f36ad8 (HEAD -> develop)
* 3d6c7e4
* b39a03f
* bfb4880
```

---

## What Does HEAD Mean?

Example:

```text
HEAD -> develop
```

Meaning:

```text
You are currently on develop.
```

---

# SECTION 10: SEEING CHANGES (`git diff`)

## What do I want to do?

See what changed before committing.

---

## Command

```powershell
git diff
```

---

## Example

Before:

```python
print("Hello")
```

After:

```python
print("Hello World")
```

Git shows:

```diff
-print("Hello")
+print("Hello World")
```

---

## Why Use It?

Before committing:

```powershell
git diff
```

lets you check:

```text
Did I change the right thing?
```

---

## View Staged Changes

```powershell
git diff --staged
```

Shows:

```text
What will be committed.
```

---

# SECTION 11: UNDO CHANGES (`git restore`)

## What do I want to do?

I changed a file.

I want the old version back.

---

## Command

```powershell
git restore filename
```

Example:

```powershell
git restore README.md
```

---

## Before

```text
README.md modified
```

---

## After

```text
README.md restored
```

---

## Warning

This deletes your unsaved changes.

Use carefully.

---

## Verify First

```powershell
git diff
```

Always look before restoring.

---

# SECTION 12: BRANCHES

## What do I want to know?

What is a branch?

---

## Simple Explanation

A branch is a separate timeline.

Example:

```text
main
```

Current working version.

---

You want to experiment:

```text
develop
```

New branch.

---

Visual:

```text
main
 │
 ├── Commit A
 ├── Commit B
 │
 └──── develop
         │
         ├── Commit C
         └── Commit D
```

---

## Why Use Branches?

Without branches:

```text
Experiment
↓
Break everything
↓
Panic
```

With branches:

```text
Experiment safely
```

---

# SECTION 13: SEE BRANCHES

## Command

```powershell
git branch
```

Example:

```text
* develop
  main
```

---

## What Does * Mean?

```text
Current branch
```

Example:

```text
* develop
```

means:

```text
You are on develop.
```

---

# SECTION 14: SWITCH BRANCHES

## What do I want to do?

Move between branches.

---

## Command

```powershell
git checkout main
```

or

```powershell
git checkout develop
```

---

## Verify

```powershell
git branch
```

Example:

```text
* main
  develop
```

---

# SECTION 15: CREATE A BRANCH

## What do I want to do?

Create a new branch.

---

## Command

```powershell
git checkout -b new_branch_name
```

Example:

```powershell
git checkout -b feature_pdf_upload
```

---

## What Happens?

Git:

1. Creates branch
2. Switches to branch

---

## Verify

```powershell
git branch
```

Example:

```text
* feature_pdf_upload
  develop
  main
```

---

# SECTION 16: DELETE A BRANCH

## What do I want to do?

Remove an old branch.

---

## Command

```powershell
git branch -d branch_name
```

Example:

```powershell
git branch -d feature_pdf_upload
```

---

## Why Delete?

Finished feature.

No longer needed.

Keep repository clean.

---

# SECTION 17: YOUR AI_PORTFOLIO BRANCH STRATEGY

You have:

```text
main
develop
```

---

## main

Think:

```text
Production
Stable
Portfolio
```

Only completed projects belong here.

---

## develop

Think:

```text
Work in Progress
Learning
Experiments
```

All new work happens here.

---

## Project Workflow

Start:

```powershell
git checkout develop
```

Build project.

Commit frequently:

```powershell
git add .
git commit -m "Add feature"
```

Push:

```powershell
git push
```

When complete:

```powershell
git checkout main
git merge develop
git push
```

---

# SECTION 18: COMMON DAILY COMMANDS CHEAT SHEET

## Where am I?

```powershell
git branch
```

---

## What's happening?

```powershell
git status
```

---

## What changed?

```powershell
git diff
```

---

## Stage everything

```powershell
git add .
```

---

## Commit

```powershell
git commit -m "Message"
```

---

## Push

```powershell
git push
```

---

## Pull

```powershell
git pull
```

---

## See history

```powershell
git log --oneline
```

---

## See beautiful history

```powershell
git log --oneline --graph --decorate --all
```

---

## Switch branch

```powershell
git checkout branch_name
```

---

## Create branch

```powershell
git checkout -b branch_name
```

---

## Delete branch

```powershell
git branch -d branch_name
```

---

# PART 2 SUMMARY

You learned:

- git add
- git commit
- git log
- git diff
- git restore
- Branches
- Creating branches
- Switching branches
- Deleting branches
- AI_Portfolio workflow

---

# BEFORE YOU COMMIT ANYTHING

Run:

```powershell
git status
git diff
git add .
git diff --staged
git commit -m "Meaningful message"
git push
```

This sequence prevents most beginner Git mistakes.

---

