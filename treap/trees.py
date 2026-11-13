# ======= trees.py =======

# ------------- BST IMPLEMENTATION ------------- #

class BSTNode:
    def __init__(self, post_id, timestamp, score):
        self.post_id = post_id
        self.timestamp = timestamp
        self.score = score
        self.left = None
        self.right = None


class BSTFeed:
    def __init__(self):
        self.root = None
        self.id_map = {}

    # ----- Public API ----- #

    def addPost(self, post_id, timestamp, score):
        if post_id in self.id_map:
            self.deletePost(post_id)
        node = BSTNode(post_id, timestamp, score)
        self.root = self._insert_iterative(self.root, node)
        self.id_map[post_id] = node

    def likePost(self, post_id):
        node = self.id_map.get(post_id)
        if node is not None:
            node.score += 1

    def deletePost(self, post_id):
        node = self.id_map.get(post_id)
        if node is None:
            return
        ts = node.timestamp
        pid = node.post_id
        self.root = self._delete_iterative(self.root, ts, pid)
        self.id_map.pop(post_id, None)

    def getMostPopular(self):
        if self.root is None:
            return None
        best = self._max_score_node(self.root)
        return (best.post_id, best.timestamp, best.score)

    def getMostRecent(self, k):
        result = []
        self._reverse_inorder_recent(self.root, k, result)
        return [(n.post_id, n.timestamp, n.score) for n in result]

    # ----- Internal helpers ----- #

    def _insert_iterative(self, root, node):
        """Iterative insert to avoid recursion depth issues."""
        if root is None:
            return node

        curr = root
        while True:
            if (node.timestamp, node.post_id) < (curr.timestamp, curr.post_id):
                if curr.left is None:
                    curr.left = node
                    break
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = node
                    break
                curr = curr.right
        return root

    def _delete_iterative(self, root, ts, post_id):
        """Fully iterative BST delete by (timestamp, post_id)."""
        if root is None:
            return None

        key = (ts, post_id)
        parent = None
        curr = root

        # 1) Find the node and its parent
        while curr is not None:
            curr_key = (curr.timestamp, curr.post_id)
            if key < curr_key:
                parent = curr
                curr = curr.left
            elif key > curr_key:
                parent = curr
                curr = curr.right
            else:
                break

        if curr is None:
            # not found
            return root

        # helper to replace child pointer from parent
        def replace_child(parent_node, old_child, new_child):
            nonlocal root
            if parent_node is None:
                root = new_child
            else:
                if parent_node.left is old_child:
                    parent_node.left = new_child
                else:
                    parent_node.right = new_child

        # 2) If node has at most one child, easy case
        if curr.left is None or curr.right is None:
            child = curr.left if curr.left is not None else curr.right
            replace_child(parent, curr, child)
            return root

        # 3) Two-children case: find inorder successor (min in right subtree)
        succ_parent = curr
        succ = curr.right
        while succ.left is not None:
            succ_parent = succ
            succ = succ.left

        # Copy successor data into current node
        curr.post_id = succ.post_id
        curr.timestamp = succ.timestamp
        curr.score = succ.score

        # Update id_map so this post_id points to curr
        self.id_map[curr.post_id] = curr

        # Now delete the successor node (succ) which has at most one child (no left)
        child = succ.right  # succ.left is None by construction
        if succ_parent.left is succ:
            succ_parent.left = child
        else:
            succ_parent.right = child

        return root

    def _min_node(self, node):
        curr = node
        while curr.left is not None:
            curr = curr.left
        return curr

    def _max_score_node(self, node):
        # iterative traversal to find max score
        stack = [node]
        best = node
        while stack:
            n = stack.pop()
            if n.score > best.score:
                best = n
            if n.left:
                stack.append(n.left)
            if n.right:
                stack.append(n.right)
        return best

    def _reverse_inorder_recent(self, node, k, acc_list):
        # iterative reverse inorder to avoid recursion
        stack = []
        curr = node
        while (stack or curr) and len(acc_list) < k:
            while curr:
                stack.append(curr)
                curr = curr.right
            curr = stack.pop()
            acc_list.append(curr)
            curr = curr.left

    def height(self):
        """Iterative height using BFS (no recursion)."""
        if self.root is None:
            return -1
        from collections import deque
        q = deque([(self.root, 0)])
        max_h = 0
        while q:
            node, h = q.popleft()
            max_h = max(max_h, h)
            if node.left:
                q.append((node.left, h+1))
            if node.right:
                q.append((node.right, h+1))
        return max_h


# ------------- TREAP IMPLEMENTATION ------------- #

class TreapNode:
    def __init__(self, post_id, timestamp, score):
        self.post_id = post_id
        self.timestamp = timestamp
        self.score = score
        self.priority = score
        self.left = None
        self.right = None


class TreapFeed:
    def __init__(self):
        self.root = None
        self.id_map = {}
        self.rotation_count = 0

    # ----- Public API ----- #

    def addPost(self, post_id, timestamp, score):
        if post_id in self.id_map:
            self.deletePost(post_id)
        node = TreapNode(post_id, timestamp, score)
        self.root = self._insert_iterative(self.root, node)
        self.id_map[post_id] = node

    def likePost(self, post_id):
        node = self.id_map.get(post_id)
        if node is None:
            return
        ts = node.timestamp
        new_score = node.score + 1
        # remove from treap structure only
        self._delete_only_tree(post_id, ts)
        # remove from map
        self.id_map.pop(post_id, None)
        # reinsert with updated score/priority
        self.addPost(post_id, ts, new_score)

    def deletePost(self, post_id):
        node = self.id_map.get(post_id)
        if node is None:
            return
        ts = node.timestamp
        self._delete_only_tree(post_id, ts)
        self.id_map.pop(post_id, None)

    def getMostPopular(self):
        if self.root is None:
            return None
        n = self.root
        return (n.post_id, n.timestamp, n.score)

    def getMostRecent(self, k):
        result = []
        self._reverse_inorder_recent(self.root, k, result)
        return [(n.post_id, n.timestamp, n.score) for n in result]

    # ----- Internal helpers ----- #

    def _insert_iterative(self, root, node):
        """Iterative treap insert (no recursion)."""
        if root is None:
            return node

        key = (node.timestamp, node.post_id)
        curr = root
        parent = None
        path = []  # stack of nodes on the search path

        # 1) Standard BST insert
        while curr is not None:
            path.append(curr)
            parent_key = (curr.timestamp, curr.post_id)
            parent = curr
            if key < parent_key:
                curr = curr.left
            else:
                curr = curr.right

        if key < (parent.timestamp, parent.post_id):
            parent.left = node
        else:
            parent.right = node

        # 2) Bubble up by priority using rotations
        child = node
        while path:
            parent = path.pop()
            if child.priority > parent.priority:
                # rotate child up
                if parent.left is child:
                    new_sub = self._rotate_right(parent)
                else:
                    new_sub = self._rotate_left(parent)

                if path:
                    grand = path[-1]
                    if grand.left is parent:
                        grand.left = new_sub
                    else:
                        grand.right = new_sub
                else:
                    root = new_sub
                # after rotation, child is the new subtree root
                child = new_sub
            else:
                break

        return root

    def _delete_only_tree(self, post_id, ts):
        self.root = self._delete_iterative(self.root, ts, post_id)

    def _delete_iterative(self, root, ts, post_id):
        """Iterative treap delete by (timestamp, post_id)."""
        if root is None:
            return None

        key = (ts, post_id)
        parent = None
        curr = root

        # 1) Find node to delete
        while curr is not None:
            curr_key = (curr.timestamp, curr.post_id)
            if key < curr_key:
                parent = curr
                curr = curr.left
            elif key > curr_key:
                parent = curr
                curr = curr.right
            else:
                break

        if curr is None:
            return root  # not found

        def replace_child(parent_node, old_child, new_child):
            nonlocal root
            if parent_node is None:
                root = new_child
            else:
                if parent_node.left is old_child:
                    parent_node.left = new_child
                else:
                    parent_node.right = new_child

        # 2) Rotate down until it has at most one child
        while curr.left is not None and curr.right is not None:
            if curr.left.priority > curr.right.priority:
                new_sub = self._rotate_right(curr)
            else:
                new_sub = self._rotate_left(curr)

            replace_child(parent, curr, new_sub)

            # curr node is still the same object; after rotation it moved
            # down as left or right child of new_sub
            if new_sub.left is curr:
                parent = new_sub
            elif new_sub.right is curr:
                parent = new_sub
            else:
                # should not happen, but guard anyway
                parent = None

        # 3) Now curr has at most one child: remove it like a BST node
        child = curr.left if curr.left is not None else curr.right
        replace_child(parent, curr, child)
        return root

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.rotation_count += 1
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.rotation_count += 1
        return y

    def _reverse_inorder_recent(self, node, k, acc_list):
        stack = []
        curr = node
        while (stack or curr) and len(acc_list) < k:
            while curr:
                stack.append(curr)
                curr = curr.right
            curr = stack.pop()
            acc_list.append(curr)
            curr = curr.left

    def height(self):
        if self.root is None:
            return -1
        from collections import deque
        q = deque([(self.root, 0)])
        max_h = 0
        while q:
            node, h = q.popleft()
            max_h = max(max_h, h)
            if node.left:
                q.append((node.left, h+1))
            if node.right:
                q.append((node.right, h+1))
        return max_h


# ------------- VALIDATION HELPERS ------------- #

def validate_bst(feed, verbose=True):
    """
    Validate BSTFeed:
    - BST property by (timestamp, post_id)
    - id_map consistency
    - reports node count and height
    """
    root = feed.root
    if root is None:
        ok = (len(feed.id_map) == 0)
        if verbose:
            print(f"BST empty. id_map size={len(feed.id_map)}. Valid: {ok}")
        return ok

    stack = []
    curr = root
    prev_key = None
    count = 0
    ok = True

    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()

        key = (curr.timestamp, curr.post_id)

        # BST order: strictly increasing keys (no duplicates)
        if prev_key is not None and key <= prev_key:
            ok = False
            if verbose:
                print("BST order violation at node:",
                      curr.post_id, "key:", key, "prev key:", prev_key)
            break
        prev_key = key

        # id_map consistency
        if curr.post_id not in feed.id_map or feed.id_map[curr.post_id] is not curr:
            ok = False
            if verbose:
                print("BST id_map mismatch for post_id:", curr.post_id)
            break

        count += 1
        curr = curr.right

    # check count vs id_map size
    if ok and count != len(feed.id_map):
        ok = False
        if verbose:
            print("BST node count mismatch:",
                  "in-tree =", count, "id_map =", len(feed.id_map))

    if verbose:
        print(f"BST valid: {ok}, nodes: {count}, height: {feed.height()}")

    return ok


def validate_treap(feed, verbose=True):
    """
    Validate TreapFeed:
    - BST property by (timestamp, post_id)
    - Heap property on priority: parent.priority >= child.priority
    - id_map consistency
    - reports node count, height, rotations
    """
    root = feed.root
    if root is None:
        ok = (len(feed.id_map) == 0)
        if verbose:
            print(f"Treap empty. id_map size={len(feed.id_map)}. Valid: {ok}")
        return ok

    stack = []
    curr = root
    prev_key = None
    count = 0
    ok = True

    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()

        key = (curr.timestamp, curr.post_id)

        # BST order
        if prev_key is not None and key <= prev_key:
            ok = False
            if verbose:
                print("Treap BST order violation at node:",
                      curr.post_id, "key:", key, "prev key:", prev_key)
            break
        prev_key = key

        # Heap property (priority)
        if curr.left and curr.left.priority > curr.priority:
            ok = False
            if verbose:
                print("Treap heap violation (left child) at node:",
                      curr.post_id, "priority:", curr.priority,
                      "left child:", curr.left.post_id,
                      "left priority:", curr.left.priority)
            break

        if curr.right and curr.right.priority > curr.priority:
            ok = False
            if verbose:
                print("Treap heap violation (right child) at node:",
                      curr.post_id, "priority:", curr.priority,
                      "right child:", curr.right.post_id,
                      "right priority:", curr.right.priority)
            break

        # id_map consistency
        if curr.post_id not in feed.id_map or feed.id_map[curr.post_id] is not curr:
            ok = False
            if verbose:
                print("Treap id_map mismatch for post_id:", curr.post_id)
            break

        count += 1
        curr = curr.right

    # check count vs id_map size
    if ok and count != len(feed.id_map):
        ok = False
        if verbose:
            print("Treap node count mismatch:",
                  "in-tree =", count, "id_map =", len(feed.id_map))

    if verbose:
        print(f"Treap valid: {ok}, nodes: {count}, height: {feed.height()}, rotations: {feed.rotation_count}")

    return ok
