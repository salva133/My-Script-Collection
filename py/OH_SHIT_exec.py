import sys
sys.path.append(r"C:\Users\Asus\OneDrive\Dokumente\GitHub\My-Script-Collection\py")
from OH_SHIT import oh_shit

if __name__ == "__main__":
    directory = r""
    
    filename = os.path.basename(__file__)
    test_mode = not ("ARMED" in filename.upper())
    oh_shit(directory, test_mode)
