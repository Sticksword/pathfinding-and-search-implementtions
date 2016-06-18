import heapq
import math

class PriorityQueue:
  def __init__(self):
    self.elements = []

  def empty(self):
    return len(self.elements) == 0

  def contains(self, item):
    return item in self.elements

  def put(self, item, priority):
    heapq.heappush(self.elements, (priority, item))

  def pop(self):
    return heapq.heappop(self.elements)[1]


class Graph:
  def __init__(self):
    self.maze = [] # matrix of all nodes
    self.start = None # start coordinates
    self.dest = None # destination coordinates

  def setup_maze(self):
    with open('input1.txt', 'r') as fp:
      final_dest = ()
      line_num = 0
      for line in fp:
        row = []
        col_num = 0
        for c in line:
          if c == '\n':
            continue
          if c == 'd':
            self.dest = (line_num, col_num)
          if c == 's':
            self.start = (line_num, col_num)
          row.append(Node(c, line_num, col_num))
          col_num += 1
        self.maze.append(row)
        line_num += 1

    if self.start is None or self.dest is None:
      raise ValueError('Input map either has no start or no destination.')

  def setup_nodes(self):
    num_rows = len(self.maze)
    num_cols = len(self.maze[0])
    for row in range(0, num_rows):
      for col in range(0, num_cols):
        # if row + 1 < num_rows and col + 1 < num_cols: # NE only if diag allowed
        #   self.maze[row][col].neighbors.append(self.maze[row + 1][col + 1])
        if col + 1 < num_cols: # E
          self.maze[row][col].neighbors.append(self.maze[row][col + 1])
        # if row - 1 >= 0 and col + 1 < num_cols: # SE
        #   self.maze[row][col].neighbors.append(self.maze[row - 1][col + 1])

        if row + 1 < num_rows: # N
          self.maze[row][col].neighbors.append(self.maze[row + 1][col])
        if row - 1 >= 0: # S
          self.maze[row][col].neighbors.append(self.maze[row - 1][col])

        # if row + 1 < num_rows and col - 1 >= 0: # NW
        #   self.maze[row][col].neighbors.append(self.maze[row + 1][col - 1])
        if col - 1 >= 0: # W
          self.maze[row][col].neighbors.append(self.maze[row][col - 1])
        # if row - 1 >= 0 and col - 1 >= 0: # SW
        #   self.maze[row][col].neighbors.append(self.maze[row - 1][col - 1])

  def manhattan_distance(self, node):
    return math.sqrt(math.pow(self.dest[0] - node.row, 2) + math.pow(self.dest[1] - node.col, 2))

  def a_star(self):
    open_list = PriorityQueue()
    closed_list = set()
    start_node = self.maze[self.start[0]][self.start[1]]
    dest_node = self.maze[self.dest[0]][self.dest[1]]
    open_list.put(start_node, 0)

    while not open_list.empty():
      current = open_list.pop()

      closed_list.add(current)

      if current == dest_node:
        print 'Destination reached! Path taken:'
        while current.parent:
          print current
          current = current.parent
        return
      
      for node in current.neighbors:
        if node in closed_list:
          continue

        elif open_list.contains(node):
          new_g = current.g + 1
          if node.g > new_g:
            node.g = new_g
            node.parent = current
            print 'new parent at %d, %d' % (node.row, node.col)

        else:
          if node.valid == True:
            node.g = current.g + 1
            node.h = self.manhattan_distance(node)
            node.parent = current
            open_list.put(node, node.g + node.h)
          else:
            closed_list.add(node)

    raise ValueError('Path unable to be found.')


class Node (object):
  def __init__(self, option, row, col):
    self.row = row
    self.col = col
    self.parent = None
    self.value = option

    if option == 's':
      self.valid = True
    elif option == 'd':
      self.valid = True
    elif option == 'o':
      self.valid = True
    else:
      self.valid = False

    self.g = 0
    self.h = 0
    self.neighbors = []

  # def __unicode__(self):
  #   return '%s' % self.value
  # reference
  # __str__ returns bytes and __unicode__ returns characters in Python 2
  # __bytes__ returns bytes and __str__ returns characters in Python 3

  def __repr__(self):
    return '(%d, %d) ' % (self.row, self.col)
  # The default implementation is useless (it’s hard to think of one which wouldn’t be, but yeah)
  # __repr__ goal is to be unambiguous
  # __str__ goal is to be readable
  # Container’s __str__ uses contained objects’ __repr__
  # Hence here, we use __repr__ since each Node will be in a container when printed

  def __eq__(self, other):
    # print other
    # other is a tuple of (priority, Node) when 'looking for Node in list'
    # other is a Node if just comparing via '=='
    if type(other) is Node:
      return self.row == other.row and self.col == other.col
    else:
      return self.row == other[1].row and self.col == other[1].col

  # since I defined __eq__, I also have to define a hash function for use in python sets
  def __hash__(self):
    return hash(self.row) ^ hash(self.col)


if __name__ == '__main__':
  maze_graph = Graph()
  maze_graph.setup_maze()
  maze_graph.setup_nodes()
  maze_graph.a_star()
