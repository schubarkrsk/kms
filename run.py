"""
Copyleft (ↄ) Stanislav Chubar, 2022. All rights reserved
Licensed under GNU GPL 3.0 license. Full text located at https://www.gnu.org/licenses/lgpl-3.0.txt

Scripts for easy to use license KEY MANAGEMENT SYSTEM (KMS) for protect 1C:Enterprise and other application
form unlicensed (cracked) using. Logic of it based on MD5's checksums
"""

import hashlib
import keyboard
import sys
import os
import time

license_and_description = "Copyleft (ↄ) Stanislav Chubar, 2022. All rights reserved\n" \
                          "Licensed under GNU GPL 3.0 license. Full text located at " \
                          "https://www.gnu.org/licenses/lgpl-3.0.txt\n\n" \
                          "Scripts for easy to use license KEY MANAGEMENT SYSTEM (KMS) for protect 1C:Enterprise and " \
                          "other application\n" \
                          "form unlicensed (cracked) using. Logic of it based on MD5's checksums"

menu_error = "Oh no... your variant not supported in this menu"
menu_lvl_0_list = "~~~MAIN MENU~~~\n" \
                  "[1] - Find trusted combination\n" \
                  "[2] - Generate licenses\n" \
                  "[3] - Exit from KMS"

menu_lvl_1and2_list = "Select generation [1 or 2]. If wish to exit press ENTER"
menu_lvl_1and2of1_list = "Enter known reg. number(RN)\n" \
                         "Important! > You RN must be mod of 6. Correct format is \"XXXXXX...XXXXXX\" or " \
                         "\"XXXXXX-...-XXXXXX\" "
menu_lvl_2of2_list = "Enter known owner name"


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def menu_find():
    print(menu_lvl_1and2_list)
    select = input(">")

    if select == "1":
        trying_with_1stgen = KMS(generation=1)
        while True:
            print(menu_lvl_1and2of1_list)
            print("Enter \":q\" to exit")
            user_inp = input(">")
            if user_inp == ":q":
                break
            if len(user_inp) % 6 == 0:
                trying_with_1stgen.set_params(reg=user_inp)
                break

        find = trying_with_1stgen.get_activation()
        key = ""
        for block in find:
            key = key + block + "-"
        key = key[:(len(key)-1)]
        print(key.upper())


    # Finish of function DON't edit!
    print("Press ESC to return into main menu")
    keyboard.wait("esc")
    clear_screen()


def menu_generate():
    print(menu_lvl_1and2of1_list)
    selected = input(">")

    # Finish of function DON't edit!
    print("Press ESC to return into main menu")
    keyboard.wait("esc")
    clear_screen()


class KMS:

    def __init__(self, generation=1):
        """
        Initialization object of KMS class
        :param generation: 1 or 2. This is using generation type. 1st based only
        """
        self.gen = generation
        self.owner = ""
        self.regnumb = ""

    def set_params(self, reg: str, owner=None):
        """
        Set parameters to find license combination
        :param reg: registration number (string mod to 6, ex. XXXXXX-XXXXXX-...-XXXXXX is N block with 6 symbols each)
        :param owner: string with name of license owner (using only in 2nd generation of licensing)
        """
        self.owner = owner
        self.regnumb = reg

    def get_activation(self, external=None):
        """
        Finding correct combination
        :return: list of N+1 blocks
        """
        if self.gen == 1:
            block_score = len(self.regnumb) // 6
            activation_blocks = []
            iteration = 1
            while block_score > 0:
                block_start = 6 * iteration - 6
                block_finish = 6 * iteration - 1
                temp_block = self.regnumb[block_start:block_finish]
                block_hash = hashlib.md5(temp_block.encode()).hexdigest()
                activation_blocks.append(block_hash[0:6])

                block_score -= 1
                iteration += 1

            checksum = ""
            for block in activation_blocks:
                checksum = checksum + block

            checksum_hash = hashlib.md5(checksum.encode()).hexdigest()
            activation_blocks.append(checksum_hash[0:6])

            return activation_blocks

        if self.gen == 2:
            pass


if __name__ == "__main__":
    print(license_and_description, "\n")
    time.sleep(3)
    while True:
        print(menu_lvl_0_list)
        selected = input(">")
        clear_screen()
        if selected == "1":
            menu_find()
        elif selected == "2":
            menu_generate()
        elif selected == "3":
            print("Goodbye! Pres ESC to close console")
            keyboard.wait("esc")
            sys.exit()
        else:
            print(menu_error)
