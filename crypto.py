def args_parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--encrypt", action='store_true',
                        help="encrypt message need a message a key file")
    parser.add_argument("--decrypt", action='store_true',
                        help="encrypt message need a message a key file")
    parser.add_argument("--message_file_name", type=str,
                        help="encrypt message need a message a key file")
    parser.add_argument("--key_file", type=str,
                        help="encrypt message need a message a key file")
    parser.add_argument("--generate_key", type=str,
                        help="encrypt message need a message a key file")

    return parser.parse_args()


def generate_key(file_name:str = "key.pem")->str:
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    print({"key": key})
    with open(file_name, 'wb') as file:
        file.write(key)
    return key


def get_key(file_name:str = "key.pem") ->bytes:
    with open(file_name, 'rb') as file:
        key = file.read()
    return key


def encrypting(message:str,
               key:str, store:bool = True,
               file_name:str = "key.pem") ->bytes:
    key = get_key(key)
    with open(message) as file:
        data = file.read()
    data = str.encode(data)
    from cryptography.fernet import Fernet
    fkey = Fernet(key)
    enc_message = fkey.encrypt(data)
    if store:
        with open(file_name, 'wb') as file:
            file.write(enc_message)
    return enc_message


def decrypt(file_name:str, key:str,
            output_file:str = "dec_message.dat",
            store:bool = True)->str:
    key = get_key(key)
    from cryptography.fernet import Fernet
    fkey = Fernet(key)
    with open(file_name,"rb") as file:
        enc_message = file.read()
    data = fkey.decrypt(enc_message)
    if store:
        with open(output_file, 'w') as file:
            file.write(enc_message.decode('utf8'))
    return data


def main():
    args = args_parser()
    if args.encrypt:
        encrypting(args.message_file_name,
                   args.key_file,
                   store=True,
                   file_name=args.enc_file_name)
    elif args.decrypt:
        decrypt(args.enc_file_name,
                args.key_file, store=True,
                output_file=args.message_file_name)
    elif args.generate_key:
        if not args.key_file:
            raise Exception("missing key_file parameters")
        generate_key(args.key_file)


FILE_NAME = "test.pem"
message = "hi from itzik"
# generate_key(FILE_NAME)
key = get_key(FILE_NAME)
# encrypting(str.encode(message), key, file_name="enc_message")
# getKey()
print(decrypt("enc_message",key))