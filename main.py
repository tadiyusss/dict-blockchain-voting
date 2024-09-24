from colorama import Fore, Style
from blockchain import Blockchain

red = Fore.RED
green = Fore.GREEN
reset = Style.RESET_ALL

blockchain = Blockchain()
if blockchain.is_valid():
    print(f"{green}Blockchain is valid{reset}")
    data = {
        "data": input("Enter a string for data: ")
    }

    print(f"Mining started {data}.")
    blockchain.add_block(data)
    print(f"Mining Finished\nIs Blockchain Valid: {blockchain.is_valid()}")

else:
    print(f"{red}Blockchain is not valid{reset}")

