from rich import print

if __name__ == "__main__":
    print('''
[bold blue]WELCOME TO THE NCA-TRAK SETUP WIZARD\n
If you haven't yet, please read the [red]README.MD [blue]file in the home directory.
[bold red]IT IS VITAL YOU HAVE THE REQUIREMENTS INSTALLED BEFORE PROCEEDING

[yellow]Please Select From the following options:
[white]
[1] Complete Install
[2] Data Regeneration
[3] Configure Data Generation Defaults
[4] Delete Database
''')
    
while(True):
    n = input()
    if not (n.isdigit() and int(n) <= 4 and int(n) > 0):
        print("[red]Please insert a number from the options listed.")
    else:
        break
n = int(n)

# TODO: Implement Each one
# Complete Install
if n == 1:
    pass
# Data Regeneration
elif n == 2:
    pass
# Configure Data Generation Defaults
elif n == 3:
    pass
# Delete Database
elif n == 4:
    pass