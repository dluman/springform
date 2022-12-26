import inspect

from Template import Template

class Factory:

    @staticmethod
    def __isdunder(name: str = "") -> bool:
        return name.startswith("__")

    def __init__(self, mod: str = "", cls: str = "", **kwargs):
        self.__mod = mod
        self.__cls = cls
        self.__props = kwargs
        self.template = Template(
            mod = self.__mod,
            cls = self.__cls
        )
        self.__elements = {
            "func": {},
            "vars": {}
        }
        self.__assemble()

    def __assemble(self) -> None:
        members = getattr(self.template, self.__mod)
        for member in inspect.getmembers(members):
            name, value = member
            if inspect.isfunction(value):
                src = inspect.getsource(value)
                self.__elements["func"][name] = src
            elif not self.__isdunder(name):
                self.__elements["vars"][name] = value

    def make(self, name: str = "") -> None:
        lines = [f"class {name}:"]
        for var in self.__elements["vars"]:
            val = self.__elements["vars"][var]
            lines.append(f"    {var} = {val}\n")
        for func in self.__elements["func"]:
            code = self.__elements["func"][func]
            lines.append(code)
        with open(f"{name}.py", "w") as fh:
            for line in lines:
                fh.write(line + "\n")
