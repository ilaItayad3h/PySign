import PySign as ps
import constants
import webbrowser
import getpass


#todo : add queries


def init():
    print(f"Welcome {getpass.getuser()} - PySign (v0.0.1) is ready to use")


def stwr():  # !!!!
    print("Some thing went wrong!")


def operationSucceed(operationName):
    return f"Operatin ({operationName}) Succeed"


def signitureIsVisibleWarning():
    return "Warning: If you continue, your signature (as .txt file) will no longer be protected and can be read by attackers"


def about():
    with open("README.md", "r") as f:
        content = f.read()
        f.close()
    print(content)


def menu():
    return """ 
        [1] Generate a pair key and Encrypt (and visualize)
        [2] Decrypt(open) key file (and visualize)
        [*] I have .txt sign file and just visualize
        [3] Report bug
        [4] About
        [0] Exit
    """


def cursor(location):
    if location == "1":  # Generate a pair key, encrypt then save file
        try:
            userNameInput = input(" Enter an arbitary user name : ")
            publicKey, privateKeyDict = ps.encrypt(
                ps.signPack(count=constants.tagPointsCount),
                ps.privateKeyDictGen(constants.rawKeysDict),
            )
            ps.saveKeys(
                username=userNameInput,
                inputEncryptedPublicKey=publicKey,
                inputEncryptedPrivateKey=privateKeyDict,
            )
            del privateKeyDict
            del publicKey
            print(operationSucceed("Generating keys and encryption"))
        except:
            privateKeyDict = None
            publicKey = None
            del privateKeyDict
            del publicKey
            stwr()
    elif location == "2":  # Decrypt(open) key file and visualize
        try:
            publicKey_FilePath = input(r"Enter public key path : ")
            privateKeyDict_Filepath = input(r"Enter private key path : ")
            publicKey, privateKeyDict = ps.readKeyFiles(
                publicKeyFilePath=publicKey_FilePath,
                privateKeyDictFilePath=privateKeyDict_Filepath,
            )
            output = ps.decrypt(
                inputEncryptedPublicKey=publicKey, inputPrivateKeyDict=privateKeyDict
            )

            del privateKeyDict
            del publicKey
            if input(f"{signitureIsVisibleWarning()} proceed? (Y/n) ").lower() == "y":
                userNameInput = input("enter an arbitary username : ")
                ps.saveDecryptedOutput(username=userNameInput, decryptedOutput=output)
                operationSucceed("saving .txt file")
            if input(" Would you like to see your sign image ? (Y/n) ").lower() == "y":
                ps.showImage(output)
                if (
                    input(
                        "would you like to save the image(.jpeg file)? (Y/n) "
                    ).lower()
                    == "y"
                ):
                    ps.saveImageFile(input("enter an arbitary username : "), output)
                    print(operationSucceed("saving image file"))
            del output
        except:
            stwr()
    elif location == '*':
        signFilePath = input(' enter sign file path (.sign): ')
        signData = ps.readSignFile(path=signFilePath)
        ps.showImage(data=signData)
    elif location == "3":  # Report Bug
        webbrowser.open("https://github.com/ilaItayad3h/PySign/issues")
    elif location == "4":  # About
        about()
    elif location == "0":  # Exit
        exit(code=0)
    else:
        print(" Invalid input ")


def launch():
    task = 2
    while KeyboardInterrupt:
        cursor(input(f"{menu()} \n > "))
        print(f"<task : {task}> \n ---------------------- \n")
        task += 1


# ----------- launcher and related

init()
print("<task : 1>")
launch()

# end of launcher
