#ifndef HOLLOW_HEAP_H
#define HOLLOW_HEAP_H

#include <algorithm>
#include <cmath>
#include <limits>
#include <vector>
#include "priority_queue.h"

// A stable item handle follows its current node through decreases.
// Old nodes remain hollow until they reach the root list.
class HollowHeap final : public PriorityQueue {
    struct Node;
    struct Item : PQNodeBase {
        Node* node;
        int value;
        Item(Node* n, int v) : node(n), value(v) {}
    };
    struct Node {
        double key;
        Item* item = nullptr;
        Node* child = nullptr;
        Node* next = nullptr;
        std::size_t rank = 0;
        explicit Node(double k) : key(k) {}
    };
    Node* roots = nullptr;
    Node* minimum = nullptr;
    int live = 0;
    std::size_t allocated = 0;

    void add_root(Node* n) {
        n->next = roots;
        roots = n;
        if (!minimum || n->key < minimum->key) minimum = n;
    }

    std::pair<double,int> erase(Item* item) {
        Node* node = item->node;
        const auto result = std::make_pair(node->key, item->value);
        node->item = nullptr;
        delete item;
        --live;
        if (node != minimum) return result;

        std::vector<Node*> ranks;
        Node* pending = roots;
        roots = minimum = nullptr;
        while (pending) {
            Node* n = pending;
            pending = n->next;
            n->next = nullptr;
            if (!n->item) {
                while (n->child) {
                    Node* child = n->child;
                    n->child = child->next;
                    child->next = pending;
                    pending = child;
                }
                delete n;
                --allocated;
                continue;
            }
            while (true) {
                if (n->rank >= ranks.size()) ranks.resize(n->rank + 1);
                Node*& peer = ranks[n->rank];
                if (!peer) {
                    peer = n;
                    break;
                }
                Node* child = peer;
                peer = nullptr;
                if (child->key < n->key) std::swap(child, n);
                child->next = n->child;
                n->child = child;
                ++n->rank;
            }
        }
        for (Node* n : ranks) if (n) add_root(n);
        return result;
    }

public:
    HollowHeap() = default;
    HollowHeap(const HollowHeap&) = delete;
    HollowHeap& operator=(const HollowHeap&) = delete;

    ~HollowHeap() override {
        while (roots) {
            Node* n = roots;
            roots = n->next;
            while (n->child) {
                Node* child = n->child;
                n->child = child->next;
                child->next = roots;
                roots = child;
            }
            delete n->item;
            delete n;
        }
    }

    PQNodeBase* insert(double key, int value) override {
        auto* node = new Node(key);
        node->item = new Item(node, value);
        add_root(node);
        ++live;
        ++allocated;
        return node->item;
    }

    bool empty() const override { return live == 0; }

    std::pair<double,int> find_min() const override {
        if (!minimum) return {std::numeric_limits<double>::infinity(), -1};
        return {minimum->key, minimum->item->value};
    }

    std::pair<double,int> extract_min() override {
        if (!minimum) return find_min();
        return erase(minimum->item);
    }

    void decrease_key(PQNodeBase* handle, double key) override {
        auto* item = dynamic_cast<Item*>(handle);
        if (!item || key >= item->node->key) return;
        if (item->node == minimum) {
            minimum->key = key;
            return;
        }
        auto* node = new Node(key);
        item->node->item = nullptr;
        item->node = node;
        node->item = item;
        add_root(node);
        ++allocated;
    }

    void remove(PQNodeBase* handle) override {
        if (auto* item = dynamic_cast<Item*>(handle)) erase(item);
    }

    int getSize() const override { return live; }
    int getHeightEstimate() const override {
        return allocated ? 1 + static_cast<int>(std::log2(allocated)) : 0;
    }
    int getNumTrees() const override {
        int count = 0;
        for (Node* n = roots; n; n = n->next) ++count;
        return count;
    }
    long long getNumCascadingCuts() const override { return 0; }
    double getMemoryUsageMBEstimate() const override {
        return (sizeof(*this) + allocated * sizeof(Node) + live * sizeof(Item)) / 1048576.0;
    }
};
#endif
