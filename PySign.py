# -------------------- Importing essential modules
import constants
from random import randint
import pickle
# from hashlib import sha256
import numpy as np
from datetime import datetime

# todo : use RSA
# todo : create a data visualization
# todo : send it to jadi


publicPath = "public key path"
privatePath = "private key path"


# -------------------- sign gen


def numberProducer(downRange: int, upRange: int):  # produces a random number
    return randint(downRange, upRange)


def labler(
    inputLable: int, inputNumber: int
):  # puts the random number produced by numberProducer in tags (indexs)
    return f"<{inputLable}>{inputNumber}</{inputLable}>"


def signPack(count: int):  # packs the numbers with assigning their lable
    signStringList = []
    for lable in range(count):
        signStringList.append(
            labler(
                inputLable=lable,
                inputNumber=numberProducer(-constants.NA, constants.NA),
            )
        )
    return signStringList


# -------------------- File


def dateTimeFormatter():  # actually this function replaces colon (:) into underscore (_) and allowing the os to save the file
    dateTimeInput = str(datetime.now())
    for dashes in range(3):
        dateTimeInput = dateTimeInput.replace("-", ".")
    for colons in range(3):
        dateTimeInput = dateTimeInput.replace(":", "_")
    return dateTimeInput


def saveKeys(
    inputEncryptedPublicKey: str, inputEncryptedPrivateKey: dict, username="Ila"
):  # saves the produced keys by encrypt function
    timeOfIssue = dateTimeFormatter()
    publicKeyFile = open(f"publicKey_{username}_{timeOfIssue}.key", "w")
    publicKeyFile.write(inputEncryptedPublicKey)
    publicKeyFile.close()
    #
    privateKeyDictFile = open(f"privateKeyDict_{timeOfIssue}.key", "wb")
    pickle.dump(inputEncryptedPrivateKey, privateKeyDictFile)
    privateKeyDictFile.close()


def readKeyFiles(
    publicKeyFilePath: str, privateKeyDictFilePath: str
):  # reads and returns public and private key files from a path
    # publicKeyFilePath = publicPath
    # privateKeyDictFilePath = privatePath
    publicKeyFile = open(publicKeyFilePath, "r")
    publicKey = publicKeyFile.read()
    publicKeyFile.close()
    #
    privateKeyFile = open(privateKeyDictFilePath, "rb")
    privateKeyDict = privateKeyFile.read()
    privateKeyFile.close()
    return publicKey, pickle.loads(privateKeyDict)


# -------------------- Crypto


def privateKeyDictGen(
    rawDict: dict,
):  # creats a private key dictionary from random string values
    privateDictKey = rawDict
    hashingStringLen = len(constants.hashingString) - 1
    hashString = ""
    for key in privateDictKey:
        for i in range(10):
            hashString += constants.hashingString[randint(0, hashingStringLen)]
        privateDictKey[key] = hashString
        hashString = ""
    return privateDictKey


def encrypt(
    inputSignList: list, inputPrivateKeyDict: dict
):  # encrypts the data using given private key dictionary
    encryptedSign = ""
    for sign in inputSignList:
        for key in inputPrivateKeyDict.keys():
            sign = sign.replace(key, inputPrivateKeyDict[key])
        encryptedSign += sign
    return encryptedSign, inputPrivateKeyDict  # enctyptedPrivateKeyDict


def getDictionaryKeyFromValue(
    dictionary: dict, val: str
):  # (Abvoius) used for decryption of the public key
    for key, value in dictionary.items():
        if val == value:
            return key
    return "Key doesn't exist"


def decrypt(
    inputEncryptedPublicKey: str, inputPrivateKeyDict: dict
):  # decrypts the given public key using its corresponding private key dictionary
    decrypteSign = ""
    for value in inputPrivateKeyDict.values():
        inputEncryptedPublicKey = inputEncryptedPublicKey.replace(
            value, getDictionaryKeyFromValue(dictionary=inputPrivateKeyDict, val=value)
        )
    return inputEncryptedPublicKey


# -------------------- tests (not part of the real program)


def Encrypt_SaveFile_oneFunciton():
    publicKey, privateKeyDict = encrypt(
        inputSignList=signPack(constants.tagPointsCount),
        inputPrivateKeyDict=privateKeyDictGen(constants.rawKeysDict),
    )

    saveKeys(
        username="Ila",
        inputEncryptedPublicKey=publicKey,
        inputEncryptedPrivateKey=privateKeyDict,
    )


def ReeadFile_Decrypt_oneFunction():
    publicKey, privateKeyDict = readKeyFiles(
        publicKeyFilePath=publicPath, privateKeyDictFilePath=privatePath
    )
    return decrypt(
        inputEncryptedPublicKey=publicKey, inputPrivateKeyDict=privateKeyDict
    )


# Encrypt_SaveFile_oneFunciton()
# print(ReeadFile_Decrypt_oneFunction)

# end of code
