import gnupg
from getpass import getpass

gpg = gnupg.GPG(gnupghome='/home/fl_rpi2/.gnupg')

# método para desencriptar archivo de codigos de acceso
def dec():
    k_p = getpass("Contraseña para acceso:")

    with open('k.gpg', 'rb') as f:
        data = str(gpg.decrypt_file(f, passphrase=k_p))
        if len(data) <= 0:
            return ""
        else:
            return(data.split("\n"))