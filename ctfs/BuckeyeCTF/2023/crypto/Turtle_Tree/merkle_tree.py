from __future__ import annotations
from abc import ABC, abstractmethod
import hashlib
import struct
import secrets
from util import *
from proof import *


class Node(ABC):
    parent: Node | None
    level: int

    @abstractmethod
    def hash(self, merkle_tree: MerkleTree) -> bytes:
        pass


class InteriorNode(Node):
    left_child: Node
    right_child: Node
    left_hash: bytes | None
    right_hash: bytes | None

    def __init__(self, parent: Node | None, level: int, prefix_bits: list[int]):
        self.parent = parent
        self.level = level

        self.left_child = EmptyNode()
        self.right_child = EmptyNode()

        self.left_child.level = level + 1
        self.left_child.parent = self
        self.left_child.index = bits_to_bytes(prefix_bits + [0])

        self.right_child.level = level + 1
        self.right_child.parent = self
        self.right_child.index = bits_to_bytes(prefix_bits + [1])

        self.left_hash = None
        self.right_hash = None

    def hash(self, merkle_tree: MerkleTree) -> bytes:
        if self.left_hash == None:
            self.left_hash = self.left_child.hash(merkle_tree)
        if self.right_hash == None:
            self.right_hash = self.right_child.hash(merkle_tree)
        return hashlib.sha256(self.left_hash + self.right_hash).digest()


class LeafNode(Node):
    index: bytes
    key: bytes
    value: bytes

    def replace_with(self, node: LeafNode):
        self.parent = node.parent
        self.level = node.level
        self.index = node.index
        self.key = node.key
        self.value = node.value

    def hash(self, merkle_tree: MerkleTree) -> bytes:
        return hashlib.sha256(
            leaf_node_identifier
            + merkle_tree.nonce
            + self.index
            + struct.pack("<I", self.level)
            + self.value
        ).digest()


class EmptyNode(Node):
    index: bytes

    def hash(self, merkle_tree: MerkleTree) -> bytes:
        return hashlib.sha256(
            empty_node_identifier
            + merkle_tree.nonce
            + self.index
            + struct.pack("<I", self.level)
        ).digest()


class MerkleTree:
    root: InteriorNode
    nonce: bytes
    root_hash: bytes

    def __init__(self):
        self.root = InteriorNode(None, 0, [])
        self.nonce = secrets.token_bytes(32)
        self.root_hash = self.root.hash(self)

    def set(self, index: bytes, key: bytes, value: bytes):
        to_add = LeafNode()
        to_add.index = index
        to_add.key = key
        to_add.value = value
        self.insert_node(index, to_add)

    def insert_node(self, index: bytes, to_add: LeafNode):
        cursor = self.root
        depth = 0
        index_bits = bytes_to_bits(index)

        while True:
            if type(cursor) is LeafNode:
                if cursor.parent == None:
                    raise ValueError("Invalid tree")

                if cursor.index == index:
                    # Replace the value
                    to_add.parent = cursor.parent
                    to_add.level = cursor.level
                    cursor.replace_with(to_add)
                    self.recompute_hash_upwards(cursor)
                    return

                new_interior_node = InteriorNode(
                    cursor.parent, depth, index_bits[:depth]
                )

                direction = get_nth_bit(cursor.index, depth)
                if direction:
                    new_interior_node.right_child = cursor
                else:
                    new_interior_node.left_child = cursor

                cursor.level = depth + 1
                cursor.parent = new_interior_node

                if type(new_interior_node.parent) is not InteriorNode:
                    raise ValueError("Invalid tree")

                if new_interior_node.parent.left_child == cursor:
                    new_interior_node.parent.left_child = new_interior_node
                elif new_interior_node.parent.right_child == cursor:
                    new_interior_node.parent.right_child = new_interior_node
                else:
                    raise ValueError("Invalid tree")
                cursor = new_interior_node

            elif type(cursor) is InteriorNode:
                direction = index_bits[depth]
                if direction:
                    if type(cursor.right_child) is EmptyNode:
                        cursor.right_child = to_add
                        to_add.level = depth + 1
                        to_add.parent = cursor
                        self.recompute_hash_upwards(to_add)
                        break
                    else:
                        cursor = cursor.right_child
                else:
                    if type(cursor.left_child) is EmptyNode:
                        cursor.left_child = to_add
                        to_add.level = depth + 1
                        to_add.parent = cursor
                        self.recompute_hash_upwards(to_add)
                        break
                    else:
                        cursor = cursor.left_child
                depth += 1
            else:
                raise ValueError("Invalid tree")

    def recompute_hash_upwards(self, node: Node):
        cursor = node
        while cursor.parent != None:
            parent = cursor.parent
            if type(parent) is not InteriorNode:
                raise ValueError("Invalid tree")

            if parent.left_child == cursor:
                direction = 0
            elif parent.right_child == cursor:
                direction = 1
            else:
                raise ValueError("Invalid tree")

            if direction:
                parent.right_hash = cursor.hash(self)
            else:
                parent.left_hash = cursor.hash(self)
            cursor = parent

        if cursor != self.root:
            raise ValueError("Invalid tree")
        self.root_hash = self.root.hash(self)

    def get(self, lookup_index: bytes) -> AuthenticationPath:
        lookup_index_bits = bytes_to_bits(lookup_index)
        depth = 0
        cursor = self.root

        auth_path = AuthenticationPath()
        auth_path.tree_nonce = self.nonce
        auth_path.lookup_index = lookup_index

        while True:
            if type(cursor) is LeafNode:
                break
            elif type(cursor) is EmptyNode:
                break
            elif type(cursor) is InteriorNode:
                direction = lookup_index_bits[depth]
                if direction:
                    if cursor.left_hash == None:
                        raise ValueError("Need to recompute hash")
                    auth_path.pruned_tree.append(cursor.left_hash)
                    cursor = cursor.right_child
                else:
                    if cursor.right_hash == None:
                        raise ValueError("Need to recompute hash")
                    auth_path.pruned_tree.append(cursor.right_hash)
                    cursor = cursor.left_child
                depth += 1
            else:
                raise ValueError("Invalid tree")

        if type(cursor) is LeafNode:
            auth_path.leaf = ProofNode()
            auth_path.leaf.level = cursor.level
            auth_path.leaf.index = cursor.index
            auth_path.leaf.value = cursor.value
            return auth_path

        elif type(cursor) is EmptyNode:
            auth_path.leaf = ProofNode()
            auth_path.leaf.level = cursor.level
            auth_path.leaf.index = cursor.index
            auth_path.leaf.value = None
            return auth_path

        else:
            raise ValueError("Invalid tree")

    def recompute_hash(self):
        self.root_hash = self.root.hash(self)
