class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

    def find(self, key):
        current = self.head
        while current:
            if current.data == key:
                return True
            current = current.next
        return False

    def delete(self, key):
        current = self.head
        if current and current.data == key:
            self.head = current.next
            current = None
            return
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next
        if current is None:
            return
        prev.next = current.next
        current = None

if __name__ == "__main__":
    ll = LinkedList()
    ll.append("Etudiant 1")
    ll.append("Etudiant 2")
    ll.append("Etudiant 3")
    ll.display()  # Output: Etudiant 1 -> Etudiant 2 -> Etudiant 3 -> None
    print(ll.find("Etudiant 1"))  # Output: True
    ll.delete("Etudiant 1")
    ll.display()  # Output: 10 -> 30 -> None