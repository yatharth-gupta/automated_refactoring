# Develop a script or tool that takes a GitHub repository and detect design smells using LLMs, creates a new branch, fix the design smells in that branch and create a pull request to the repository.
# The script will be run by the user and will output a list of design smells in the codebase.

import os
import shutil
from github import Github
from github import Auth
import google.generativeai as genai

context = """
Abstraction

Missing Abstraction: An instance where an abstraction should be present but is not.
Unnecessary Abstraction: Abstraction that is not needed and does not provide a clear benefit.
Imperative Abstraction: Abstraction that unnecessarily describes the details of its implementation.
Incomplete Abstraction: An abstraction that does not provide a complete set of functionalities, requiring its users to know about its internals.
Multifaceted Abstraction: An abstraction that has more than one responsibility, violating the single responsibility principle.
Unutilized Abstraction: An abstraction that is defined but never used.
Duplicate Abstraction: Multiple abstractions that serve the same purpose.

Encapsulation

Deficient Encapsulation: The internal details of the class are not properly hidden, violating encapsulation.
Leaky Encapsulation: Encapsulation is present but some internal details are unnecessarily exposed.
Missing Encapsulation: There is no encapsulation; data members are public or easily accessible.
Unexploited Encapsulation: Encapsulation is present but not fully leveraged, leading to redundant code elsewhere.

Modularization

Broken Modularization: Modules do not encapsulate a single, coherent set of behaviors.
Insufficient Modularization: A module does not provide a clear, focused subset of the system's functionality.
Cyclically-dependent Modularization: Modules depend on each other in a circular manner, making it impossible to consider them independently.
Hub-like Modularization: A module that acts as a central point of communication or control, creating a bottleneck.

Hierarchy

Missing Hierarchy: A hierarchy is expected or would be beneficial, but is not present.
Unnecessary Hierarchy: A hierarchy that is over-engineered and provides no clear benefit.
Unfactored Hierarchy: A hierarchy that has not been properly refactored, containing duplicate code across different levels.
Wide Hierarchy: A hierarchy with too many siblings, indicating poor abstraction choices.
Speculative Hierarchy: A hierarchy based on speculation of future use rather than actual requirements.
Deep Hierarchy: A hierarchy with too many levels of inheritance, making it difficult to navigate or understand.
Rebellious Hierarchy: A subclass does not follow the anticipated or intended behavior of its superclass.
Broken Hierarchy: A hierarchy where subclasses do not logically belong to their superclasses.
Multipath Hierarchy: A hierarchy with multiple inheritance paths to the same class, causing ambiguity.
Cyclic Hierarchy: A hierarchy with cycles, which should not happen in a well-designed class structure."""

# Clone the repository
def clone_repo(repo_url, repo_name):
    # if the repository already exists, delete it
    if os.path.exists(repo_name):
        shutil.rmtree(repo_name)
    os.system('git clone ' + repo_url + ' ' + repo_name)

# Create a new branch
def create_branch(repo_name, branch_name):
    os.chdir(repo_name)
    os.system('git checkout -b ' + branch_name)
    os.chdir('..')

# Add, commit, and push changes
def add_commit_push(repo_name, branch_name,g,owner_repo):
    # check if remote branch already exists, delete it
    repo = g.get_repo(owner_repo)
    branches = list(repo.get_branches())
    branch_exists = False
    for branch in branches:
        if branch.name == branch_name:
            branch_exists = True
            break

    if branch_exists:
        os.chdir(repo_name)
        os.system('git push origin --delete ' + branch_name)
        os.chdir('..')

    # Add, commit, and push changes
    os.chdir(repo_name)
    os.system('git add .')
    os.system('git commit -m "Fix design smells"')
    os.system('git push origin ' + branch_name)
    os.chdir('..')
    

# Create a pull request
def create_pull_request(repo_name, branch_name, pr_title, pr_body,g,owner_repo):
    try:
        # Get the repository
        repo = g.get_repo(owner_repo)

        # Create a pull request
        pull_request = repo.create_pull(title=pr_title, body=pr_body, head=branch_name, base='main')
        print("Pull request created:", pull_request.html_url)
    except Exception as e:
        print(f"Error creating pull request: {str(e)}")

# Find design smells in .java files
def design_smells(repo_name, branch_name,g,owner_repo):
    pr_title = "Fix design smells"
    GOOGLE_API_KEY= os.environ.get('GOOGLE_API_KEY')

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.0-pro-latest')

    # Get the list of .java files in the repository
    java_files = []
    for root, dirs, files in os.walk(repo_name):
        for file in files:
            if file.endswith('.java'):
                java_files.append(os.path.join(root, file))

    # Read the content of each .java file and find design smells
    for file in java_files:
        with open(file, 'r+') as f:
            code = f.read()
            chat = model.start_chat(history=[])
            response = chat.send_message(f"I am proving you with all possible design smells, use only them and your knowledge about them to list and explain in brief the design smells in code which will be provided in future prompts. Design Smells: \n {context}. /n You can use your knowledge of given smells to list and explain the design smells in the code.")
            # print("first response:",response.text)
            # print()

            prompt = f"Just List and explain design smells in the below code: \n {code}. \n Don't suggest any fixes, just list and explain the design smells."
            response = chat.send_message(prompt)
            # to_markdown(result.text)
            print("second response:",response.text)
            print()

            # fix the design smells
            response = chat.send_message("Refactor the design smells you listed in the above code and provide the whole refactored code while preserving same functionalities as before, do not add or remove any functionality. The code given by you will go in production directly. So be responsible, the code should work and compile. Only provide code nothing else.")
            print("third response:",response.text)

            # code is in form ```java ... ```
            refactored_code = response.text.split('```')[1]
            
            java = "java\n"
            refactored_code = refactored_code[len(java):]

            comment = response.text.split('```')[0] + response.text.split('```')[2]

            # replace the original code with the refactored code
            f.seek(0)
            f.write(refactored_code)
            f.truncate()

            # add commit push
            add_commit_push(repo_name, branch_name, g, owner_repo)

            # create pull request
            create_pull_request(repo_name, branch_name, pr_title, comment,g,owner_repo)

# Delete the repository
def delete_repo(repo_name):
    shutil.rmtree(repo_name)

# Main function
def main():

    repo_url = "https://github.com/ManujGarggit/test"
    repo_name = "automated_refactoring"
    branch_name = "fix_design_smells-1"
    pr_title = "Fix design smells"
    pr_body = "Fixing design smells in the codebase"
    owner = repo_url.split('/')[-2]
    repo = repo_url.split('/')[-1]

    # Authenticate with GitHub, use token from workflow
    github_token = os.environ.get('GITHUB_TOKEN')

    auth = Auth.Token(github_token)

    g = Github(auth = auth)

    clone_repo(repo_url, repo_name)
    create_branch(repo_name, branch_name)
    design_smells(repo_name,branch_name,g,owner + '/' + repo)
    # delete_repo(repo_name)  # Optionally delete the repository after creating the pull request

if __name__ == "__main__":
    main()
