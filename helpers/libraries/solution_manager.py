from abc import ABC, abstractmethod
import importlib
import os


class PuzzleSolution(ABC):
    @abstractmethod
    def get_answer_a(self, input: str) -> int | float | str:
        pass

    @abstractmethod
    def get_answer_b(self, input: str) -> int | float | str:
        pass
    

class SolutionManager:
    def __init__(self, solution_path: str, class_name: str):
        self.module_path = solution_path
        self.class_name = class_name
        
        self.solution : PuzzleSolution | None = None 

    def load_solution(self):
      print(f"🔃 Loading class '{self.class_name}' from '{self.module_path}'... ", end="", flush=True)

      module_name = os.path.splitext(os.path.basename(self.module_path))[0]
    
      try:  
        class_defintion = SolutionManager.get_class_definition(self.module_path, module_name, self.class_name)
        self.solution = class_defintion()
      except Exception:
        print("⚠️  Loading class failed.")
        self.solution = None
        return  

      print("Done!")

    def get_class_definition(module_path, module_name, class_name):
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module) 
        class_defintion = getattr(module, class_name)
        return class_defintion
    
    def run_solution_a(self, input:str):
        if self.solution is None:
            print("⚠️  No solution loaded yet.") 
            return
        
        return self.solution.get_answer_a(input)
    
    def run_solution_b(self, input:str):
        if self.solution is None:
            print("⚠️  No solution loaded yet.") 
            return
        
        return self.solution.get_answer_b(input)