#include <vector>
#include <unordered_map>
#include <iostream>

template<typename Key_t, typename Value_t>
class LruCache {
private:
	struct Entry_t {
		Key_t Key;
		Value_t Value;
		Entry_t *Next;
		Entry_t *Prev;
	};

	Entry_t *m_Storage;
	Entry_t *m_Head, *m_Tail;
	std::vector<Entry_t*> m_FreeEntries;
	std::unordered_map<Key_t, Entry_t*> m_Cache;
	size_t m_Size;

	void Unlink(Entry_t *Entry) {

		//
		// Unlink the current entry.
		//

		Entry->Prev->Next = Entry->Next;
		Entry->Next->Prev = Entry->Prev;
	}

	void Promote(Entry_t *Entry) {

		//
		// Promote the entry to the head.
		//

		Entry->Next = m_Head->Next;
		Entry->Prev = m_Head;
		m_Head->Next->Prev = Entry;
		m_Head->Next = Entry;
	}

	void Evict() {

		//
		// The least recently used entry is at the tail.
		//

		Entry_t *LeastRecentlyUsed = m_Tail->Prev;
		Unlink(LeastRecentlyUsed);

		//
		// The entry is now free.
		//

		m_FreeEntries.emplace_back(LeastRecentlyUsed);
		m_Cache.erase(LeastRecentlyUsed->Key);
	}

public:
	LruCache(const size_t MaxSixe) {
		m_Size = MaxSixe;
		m_Cache.rehash(MaxSixe);
		m_FreeEntries.reserve(MaxSixe);
		m_Storage = new Entry_t[MaxSixe];
		for (size_t i = 0; i < MaxSixe; ++i) {
			m_FreeEntries.emplace_back(m_Storage + i);
		}
		m_Head = new Entry_t;
		m_Tail = new Entry_t;
		m_Head->Next = m_Tail;
		m_Head->Prev = nullptr;
		m_Tail->Next = nullptr;
		m_Tail->Prev = m_Head;
	}

	const Value_t* Get(const Key_t &K) {
		auto It = m_Cache.find(K);
		if (It == m_Cache.end()) {
			return nullptr;
		}

		Unlink(It->second);
		Promote(It->second);
		return &It->second->Value;
	}

	const Value_t* Put(const Key_t &K, const Value_t &V) {
		if (m_Cache.size() >= m_Size) {

			//
			// We need to evict the least used entry.
			//

			Evict();
		}

		//
		// Grab a free entry.
		//

		Entry_t *Entry = m_FreeEntries.back();
		m_FreeEntries.pop_back();
		Entry->Key = K;
		Entry->Value = V;

		//
		// Promote it to the head now.
		//

		Promote(Entry);

		//
		// Store it in the cache.
		//

		m_Cache.emplace(K, Entry);
		return &Entry->Value;
	}

	~LruCache() {
		delete[] m_Storage;
		delete m_Head;
		delete m_Tail;
		m_FreeEntries.clear();
		m_Cache.clear();
	}
};

int main() {
	LruCache<uintptr_t, const char*> Cache(2);
	Cache.Put(1, "one");
	Cache.Put(2, "two");
	std::cout << *Cache.Get(1);
	std::cout << *Cache.Get(2);
	Cache.Put(4, "four");
	std::cout << *Cache.Get(4);
	return EXIT_SUCCESS;
}