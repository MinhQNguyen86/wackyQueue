"""
# Copyright Minh Nguyen, 2018
# Copyright Nick Cheng, 2018
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSCA48, Winter 2018
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

from wackynode import WackyNode

# Do not add import statements or change the one above.
# Write your WackyQueue class code below.


class WackyQueue():
    '''A Priority Queue consisting of WackyNodes'''

    def __init__(self):
        '''(WackyQueue) -> NoneType
        Creates an empty WackyQueue
        '''
        # Representation Invariant:
        # WackyQueue items are stored as two linked list
        # self._odd points to a linked list of every odd WackyNode
        # self._even points to a linked list of every even WackyNode
        # If self._odd and self._even equals None
        #    WackyQueue is empty

        self._odd = None
        self._even = None

    def insert(self, obj, pri):
        '''(WackyQueue, obj, int) -> NoneType
        Creates a new WackyNode and inserts it into the
        WackyQueue sorted descendingly. Items with
        the same priority are sorted according to which
        item was added first.
        '''
        # Create node
        node = WackyNode(obj, pri)

        # Insert first item
        if self._odd is None:
            self._odd = node
        # Insert the second item if
        # it has less priority than first
        elif self._even is None and node.get_priority(
                ) <= self._odd.get_priority():
            self._even = node
        # Switch the first and second if
        # second node has greater priority
        elif self._even is None and node.get_priority(
                ) > self._odd.get_priority():
            self._even = self._odd
            self._odd = node
        # Insert the nth item, where n > 2
        else:
            # Store the first and second nodes
            cur_node1 = self._odd
            cur_node2 = self._even
            # Keep track of the size of both lists
            sizeodd = 1
            sizeeven = 1

            # Take the nodes with the highest possible
            # priority from both lists
            while (cur_node1.get_next() is not None and (
                    cur_node1.get_next().get_priority(
                        ) >= node.get_priority())):
                sizeodd += 1
                cur_node1 = cur_node1.get_next()

            while (cur_node2.get_next() is not None and (
                    cur_node2.get_next().get_priority(
                        ) >= node.get_priority())):
                sizeeven += 1
                cur_node2 = cur_node2.get_next()

            # First Case:
            # The current nodes priorities taken from the
            # even and odd lists are greater than or equal
            # to the node priority
            if (cur_node1.get_priority() >= node.get_priority(
                    ) and cur_node2.get_priority() >= node.get_priority()):
                # Find greater value between two current nodes
                # By default assume the odd list contains the higher node
                greatest = cur_node1
                lowest = cur_node2
                if cur_node1.get_priority() < cur_node2.get_priority():
                    greatest = cur_node2
                    lowest = cur_node1
                elif cur_node1.get_priority() == cur_node2.get_priority():
                    # If odd list is longer, add node to the even list
                    if sizeodd > sizeeven:
                        greatest = cur_node2
                        lowest = cur_node1

                temp = greatest.get_next()
                greatest.set_next(node)
                node.set_next(lowest.get_next())
                lowest.set_next(temp)

            # Second Case:
            # The node priority is strictly inbetween the two
            # priorities or equal to the first odd node's priority
            elif (cur_node1.get_priority() >= node.get_priority(
                    ) and cur_node2.get_priority() < node.get_priority()):
                # Insert in between
                temp = cur_node1.get_next()
                cur_node1.set_next(cur_node2)
                self._even = node
                node.set_next(temp)

            # Third Case:
            # The node priority is strictly greater than both
            elif (cur_node1.get_priority() < node.get_priority(
                    ) and cur_node2.get_priority() < node.get_priority()):
                # Insert at the beginning
                temp = cur_node1
                self._odd = node
                node.set_next(cur_node2)
                self._even = temp

    def extracthigh(self):
        '''(WackyQueue) -> WackyNode
        Return the highest prioritized WackyNode
        REQ: WackyQueue is not empty
        '''
        # Assign high to None in case WackyQueue is empty
        high = None
        if not self.isempty():
            high = self._odd
            self._odd = self._even
            self._even = high.get_next()
        return high

    def isempty(self):
        '''(WackyQueue) -> bool
        Returns a boolean value that shows if WackyQueue
        is empty
        '''
        empty = False
        if self._odd is None and self._even is None:
            empty = True
        return empty

    def changepriority(self, obj, pri):
        '''(WackyQueue, obj, int) -> NoneType
        If obj is in the queue and priority is not already pri,
        change the first copy of obj's priority
        '''
        # Points to current node
        nodd = self._odd
        neven = self._even
        # Points to previous nodes before desired
        # node; used to check if node is at the start
        # of either list (node1/node2 will remain None)
        node1 = None  # Odd
        node2 = None  # Even

        # Loop through both lists trying to find desired
        # node whose value equals to obj
        while (nodd is not None or neven is not None) and (
                nodd.get_item() != obj and neven.get_item() != obj):
            # Makes sure to get the last node of the odd list
            # A C E
            # B D
            if neven is None:
                node1 = nodd
                nodd = nodd.get_next()
            else:
                # node1/2 holds the node before desired node
                # (A) C E
                # (B) D F
                # C is desired
                node2 = neven
                neven = neven.get_next()
                node1 = nodd
                nodd = nodd.get_next()

        # 1.) If nodd/neven is None then the obj is
        # not in the list
        # 2.) If the obj is in the list and it's changed
        # priority is different..
        if nodd is not None and nodd.get_item(
                ) == obj and nodd.get_priority() != pri:
            # Case 1:
            # Desired node is the first node in the odd list
            # self._odd
            if node1 is None:
                # Removes the desired node for
                # garbage collection
                # Insert the a new node with
                # new priority
                node1 = nodd
                node2 = neven
                # Set the beginning of the even
                # and odd lists to the correct new
                # nodes
                self._odd = node2
                self._even = node1.get_next()
                node1.set_next(None)
                self.insert(obj, pri)
            else:
                node1.set_next(node2.get_next())
                node2.set_next(nodd.get_next())
                nodd.set_next(None)
                self.insert(obj, pri)
        elif neven is not None and neven.get_item(
                ) == obj and neven.get_priority() != pri:
            # Case 2:
            # Desired node is first node in even list
            if node2 is None:
                # Set the start of the even list
                # to correct new node
                node1 = nodd
                node2 = neven
                self._even = node1.get_next()
                node1.set_next(node2.get_next())
                node2.set_next(None)
                self.insert(obj, pri)
            else:
                temp = node1.get_next().get_next()
                node1.get_next().set_next(neven.get_next())
                node2.set_next(temp)
                neven.set_next(None)
                self.insert(obj, pri)

    def negateall(self):
        '''(WackyQueue) -> NoneType
        Reverses the priority of the WackyQueue
        '''
        # Reverse the two lists, and assign new heads
        self._odd = self.reverse(self._odd)
        self._even = self.reverse(self._even)

        # Check which list has the greatest priority,
        # then assign that as self._odd
        if (self._odd.get_priority() < self._even.get_priority()):
            self._odd, self._even = self._even, self._odd

    def getoddlist(self):
        '''(WackyQueue) -> WackyNode
        Returns the first odd WackyNode
        '''
        return self._odd

    def getevenlist(self):
        '''(WackyQueue) -> WackyNode
        Returns the first even WackyNode
        '''
        return self._even

    def __str__(self):
        '''(WackyQueue) -> str
        Returns a string representation
        of the Queue
        '''
        cur1 = self.getoddlist()
        cur2 = self.getevenlist()
        temp = "odd: "
        temp2 = "even: "

        while cur1 is not None:
            temp += str(cur1.get_item()) + " "
            cur1 = cur1.get_next()

        while cur2 is not None:
            temp2 += str(cur2.get_item()) + " "
            cur2 = cur2.get_next()

        return temp + "\n" + temp2

    def reverse(self, node):
        '''(WackyQueue, WackyNode) -> NoneType
        Reverses the linked list, given the first node
        of that list
        '''
        # To be head of new list
        n = None
        # Loop through until end is reached
        while node is not None:
            curr = node
            node = node.get_next()
            # Negates the priority
            curr.set_priority(curr.get_priority()*-1)
            curr.set_next(n)
            n = curr
        return n
