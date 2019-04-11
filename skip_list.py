from random import random

class SkipList:
    """
    Skip-List.
    """

    class Element:
        """
        Skip-List element.
        """

        def __init__(self, value, height):
            """
            Generates a skip-list element.
            """
            self.value = value
            self.quantity = 1
            self.next = [None]*height
        

    def __init__(self):
        """
        Generates an empty skip-list.
        """
        self.head = self.Element(float("-inf"), height = 0)
        self.tail = self.Element(float("inf"),  height = 0)
        self.numElements = 0
        self.head.next.append(self.tail)


    @staticmethod
    def randomHeight():
        """
        Generates a random height with distribution
        Prob(h = k) = 2^(-k).
        """
        height = 1
        while random() < 0.5:
            height += 1
        return height


    def searchPath(self, value):
        """
        Let path be the path returned by this method,
        then path[h] stores the last element visited
        at height h during the search of value through
        the skip-list.
        """
        element = self.head
        path = [None]*len(self.head.next)
        for h in range(len(self.head.next)-1, -1, -1):
            while element.next[h].value < value:
                element = element.next[h]
            path[h] = element
        return path


    def search(self, value):
        """
        Returns the element containing value, if
        value is present in the skip-list. Returns
        None otherwise.
        """
        predecessor = self.searchPath(value)
        target = predecessor[0].next[0]
        return target if target.value == value else None
    

    def __contains__(self, value):
        """
        Checks whether value is present in the skip-list.
        """
        return self.search(value) != None


    def insert(self, value):
        """
        Inserts value into the skip-list.
        """
        predecessor = self.searchPath(value)
        target = predecessor[0].next[0]
        self.numElements += 1
        
        if target.value == value:
            target.quantity += 1
            return

        height = self.randomHeight()
        newElement = self.Element(value, height)

        for h in range(len(predecessor), height):
            self.head.next.append(self.tail)
            predecessor.append(self.head)

        for h in range(height):
            newElement.next[h] = predecessor[h].next[h]
            predecessor[h].next[h] = newElement


    def delete(self, value):
        """
        Deletes one entry of value in the skip-list.
        """
        predecessor = self.searchPath(value)
        target = predecessor[0].next[0]

        if target.value != value:
            return

        self.numElements -= 1

        if target.quantity > 1:
            target.quantity -= 1
            return

        for h in range(len(target.next)):
            predecessor[h].next[h] = target.next[h]
            if predecessor[h] is self.head and predecessor[h].next[h] is self.tail:
                del self.head.next[max(1, h):]
                break


    def __iter__(self):
        """
        Iterator over the element in the skip-list.
        """
        element = self.head.next[0]
        while len(element.next) > 0:
            yield element
            element = element.next[0]


    def __len__(self):
        """
        Returns the number of unique elements in
        the skip-list.
        """
        return self.numElements


    def _repr_level(self, l):
        """
        Represents the l-th level in the skip-list.
        """
        return" ".join(["-inf"]
                      +["-"*len(str(x.value)) if l > len(x.next)-1 else str(x.value) for x in self]
                      +["+inf"]) 


    def __repr__(self):
        """
        Represents the skip-list.
        """
        return "\n".join(self._repr_level(l) for l in range(len(self.head.next)-1, -1, -1))

