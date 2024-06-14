from brownie import Crop
from brownie import accounts
# from scripts import integrate

def main(path):
    account = accounts[0]
    ss= Crop.deploy({"from": account})
    print(ss)
    # integrate.addrecord()
    


    