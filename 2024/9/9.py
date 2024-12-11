from enum import Enum
from turtle import pos
from typing import List, Tuple

from attr import has
from libraries.solution_manager import PuzzleSolution

class StorageType(Enum):
    EMPTY = 0
    FILE = 1

class StorageBlock:
    def __init__(self, storage_type: StorageType, size: int, id: int = None):
        self.storage_type = storage_type
        self.id = id
        self.size = size
        self.is_defragged = False

        if storage_type == StorageType.EMPTY and id is not None:
            raise Exception("Empty sectors cannot have id")

    def __repr__(self):
        if self.storage_type == StorageType.FILE:
            return "".join([str(self.id) for _ in range(self.size)])
            # return "".join(["#" for _ in range(self.size)])
        if self.storage_type == StorageType.EMPTY:
            return "".join(["." for _ in range(self.size)])

class Storage:
    def __init__(self):
        self.expecting_block_type = StorageType.FILE
        self.expecting_block_id = 0
        self.blocks: List[StorageBlock] = []

    def add_block(self, size: int):
        if size == 0:
            self.toggle_expecting_block_type()
            return

        if self.expecting_block_type == StorageType.FILE:
            self.blocks.append(StorageBlock(self.expecting_block_type, size, self.expecting_block_id))
            self.expecting_block_id += 1
            self.toggle_expecting_block_type()
            return 
        
        if self.expecting_block_type == StorageType.EMPTY:
            self.blocks.append(StorageBlock(self.expecting_block_type, size))
            self.toggle_expecting_block_type()
            return

    def toggle_expecting_block_type(self):
        if self.expecting_block_type == StorageType.FILE:
            self.expecting_block_type = StorageType.EMPTY
            return
        if self.expecting_block_type == StorageType.EMPTY:
            self.expecting_block_type = StorageType.FILE
            return

    def __repr__(self):
        result = ""
        for block in self.blocks:
            result += str(block)
        return result 

    def get_first_undefragged_empty_block_before_file(self, before_file):
        for block in self.blocks:
            if block == before_file:
                return None
            if block.storage_type == StorageType.EMPTY and not block.is_defragged:
                return block

        return None
    
    def get_last_undefragged_file_block(self):
        reversed = list(self.blocks)
        reversed.reverse()

        for block in reversed:
            if block.storage_type == StorageType.FILE and not block.is_defragged:
                return block

        return None
    
    def has_no_fragmentation(self):
        has_seen_empty = False

        for block in self.blocks:
            if has_seen_empty and block.storage_type == StorageType.FILE:
                return False
            
            if block.storage_type == StorageType.EMPTY:
                has_seen_empty = True

        return True

    def split(self, block, size_of_first):
        for i in range(len(self.blocks)):
            found_block = self.blocks[i]
            if found_block == block:
                if size_of_first >= found_block.size:
                    raise Exception("cannot split block because requested size is larger or same as block size")
                if size_of_first == 0:
                    raise Exception("cannot split block because requested size is zero")
                
                new_empty_block = StorageBlock(storage_type=StorageType.EMPTY, size=found_block.size - size_of_first)
                found_block.size = size_of_first

                self.blocks = self.blocks[:i] + [found_block, new_empty_block]  + self.blocks[i+1:] 
                return found_block, new_empty_block
        
        raise Exception("Did not find block")

    def defrag(self):
        file = self.get_last_undefragged_file_block()
        empty = self.get_first_undefragged_empty_block_before_file(file)

        if empty is None:
            raise Exception("Not empty found")
        if file is None:
            raise Exception("Not file found")


        if file.size == empty.size:
            empty.id = file.id
            empty.storage_type = StorageType.FILE
            file.storage_type = StorageType.EMPTY
            return

        if file.size > empty.size:
            empty.id = file.id
            empty.storage_type = StorageType.FILE
            self.split(file, file.size - empty.size)
            return

        if file.size < empty.size:
            empty.id = file.id
            empty.storage_type = StorageType.FILE
            self.split(empty, file.size)
            file.storage_type = StorageType.EMPTY
            return
        
    def reset_empty_defrag_flags(self):
        for block in self.blocks:
            if block.storage_type == StorageType.EMPTY:
                block.is_defragged = False

    def defrag_file(self):
        file = self.get_last_undefragged_file_block()
        empty = self.get_first_undefragged_empty_block_before_file(file)

        while empty is not None:

            if empty is None:
                raise Exception("No empty found")
            if file is None:
                raise Exception("No file found")

            if file.size == empty.size:
                empty.id = file.id
                empty.storage_type = StorageType.FILE
                empty.is_defragged = True
                file.storage_type = StorageType.EMPTY
                break

            if file.size < empty.size:
                empty.id = file.id
                empty.storage_type = StorageType.FILE
                empty_part_a, empty_part_b = self.split(empty, file.size)
                empty_part_a.is_defragged = True
                empty_part_b.is_defragged = True
                file.is_defragged = True
                file.storage_type = StorageType.EMPTY
                break

            empty.is_defragged = True
            empty = self.get_first_undefragged_empty_block_before_file(file)
        
        file.is_defragged = True
        self.reset_empty_defrag_flags()


    def remove(self, block):
        self.blocks.remove(block)

    def hash(self):
        product_sum = 0
        position = 0
        for block in self.blocks:
            for _ in range(block.size):
                if block.storage_type == StorageType.FILE and block.size > 0:
                    product_sum += position * block.id
                position += 1
        
        return product_sum

class Solution(PuzzleSolution):
    
    def get_answer_a(self, input: str) -> int | float | str:
        storage = self.get_elements(input)
        
        # print(storage)
        
        iteration = 0
        while not storage.has_no_fragmentation():
            iteration += 1
            if iteration > 100000:
                raise Exception("Iteration count exceeded")

            storage.defrag()
            print(storage)

        # print(storage)
        return storage.hash()

    def get_answer_b(self, input: str) -> int | float | str:
        storage = self.get_elements(input)
        
        # print(storage)
        
        iteration = 0
        while not storage.has_no_fragmentation():
            iteration += 1
            if iteration > 100000:
                raise Exception("Iteration count exceeded")

            try:
                storage.defrag_file()
            except Exception as e:
                print(f"Defrag ended because of exception: {e}")
                break
            # print(storage)

        # print(storage)
        return storage.hash()
    
    @staticmethod
    def get_elements(input: str):
        storage = Storage()

        for number in map(int, input):
            storage.add_block(number)

        return storage