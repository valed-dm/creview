class Switch:
    bvalue = True

    def switch(self):
        res = not self.bvalue
        self.bvalue = res
        return res


switch = Switch()
