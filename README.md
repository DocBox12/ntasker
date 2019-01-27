# ntasker
Ntasker is application for automatic addes tasks to Nozbe. 

# The goal of the project

I am using Nozbe to planning every day but this project have a one bugs - if we use a repeating task function and we will add to one task a one category it all tasks have the assigned category.

**Example:**

We added task "Buy bread" and we setting, that it is everyday task. We added a category, we finished task but tomorrow we have task "Buy bread" with added category from yesterday. The category has been added to all repetitive tasks. It annoyed me and that's why this program was created.

# Requirements

- Python3
- Virtualenv Python3
- Nozbe account
- Email account

# Usage

- create Python3 venv
- download latest version from Stable branch (if you want use the development version, clone master branch)
- extract archive 
- go to the src directory
- run `chmod +x ntasker.py`
- configure config.ini and tasks.json
- run `ntasker.py`

# Files descriptions

**ntasker.py**

It is a main program. Run it if you want run program.

**config.ini**

This is configuration file. In the file you must give information about your email account from you be send messages to nozbe.

```text
server = The name of the SMTP server
username = Email username
password = Password for email account
port = Server port, probably 465
address = Your nozbe address. You find this in nozbe settings.
```

**tasks.json**

In the file you add all tasks which they will be sent to nozbe. The file is divided for days of the week and for every you can add other tasks. Remember, if you run program  in Saturday, only tasks added to Saturday has be send to your Nozbe account.

# Configure tasks syntax

To add task you must use a specific syntax. It looks like this:

"Title task":"comment task"

**Example:**

```json
{
    "Monday": [
        {
            "Buy bread":"Buy bread in a bakery on the street Washington",
            "Read a book":"I must finish read a book"
        }
    ],
```

Remember: any task that is not last must have comma in the end. If you forget add comma the program will return error:

```text
Expecting property name enclosed in double quotes: line 233 column 9 (char 11102)
```

Line means in which place you made a mistake.

## Checklist in tasks

Nozbe allows added task which have checklists and this program  can do created that tasks. 

Example:

```json
{
    "Monday": [
        {
            "Do shopping":"checklist: \n (-) Buy bread \n (-) Buy shoes \n (-) Buy medicines"
        }
    ],
```

`checklist:` is requirements to Nozbe.

`\n` this create new line between checklist and your task

`(-)` Ten symbol sprawia, że twoje zadania nie są zaznaczone.

`Buy bread` Your task

This syntax after execute program it look like this: 

```text
checklist:
Buy bread
Buy shoes
Buy medicines
```

Next this text is added to email content and send to your nozbe account. When Nozbe receives a message,he will create a task "Do shopping" which will have be a checklist.

## Create comments

JSON not support comments, but this program it support. If you want add comment use it: 

```text
"___comment___":"Your comment"
```

This syntax will be treated as comment, not task.