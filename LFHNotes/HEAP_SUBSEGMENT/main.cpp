#include <windows.h>
#include <stdio.h>

#include <ctime>
#include <vector>
#include <new>

// Don't forget that the chunk header is 8 bytes long, so the allocations will be store in the (64+8) bucket
#define SIZE (64)
#define ENABLE_LFH_N (0x12)

/// .load D:\Codes\LFHNotes\Debug\LFHViewer.dll

int main()
{
	HANDLE hHeap = INVALID_HANDLE_VALUE;
	std::vector<void*> alloc;

	hHeap = HeapCreate(0, 0, 0);
	/*
		0:000> dt nt!_HEAP @@(hHeap)
		ntdll!_HEAP
		   +0x000 Entry            : _HEAP_ENTRY
		   +0x008 SegmentSignature : 0xffeeffee
		   +0x00c SegmentFlags     : 2
		   +0x010 SegmentListEntry : _LIST_ENTRY [ 0x6c00a4 - 0x6c00a4 ]
		   +0x018 Heap             : 0x006c0000 _HEAP
		   +0x01c BaseAddress      : 0x006c0000 Void
		   +0x020 NumberOfPages    : 0xf
		   +0x024 FirstEntry       : 0x006c0498 _HEAP_ENTRY
		   +0x028 LastValidEntry   : 0x006cf000 _HEAP_ENTRY
		   +0x02c NumberOfUnCommittedPages : 0xa
		   +0x030 NumberOfUnCommittedRanges : 1
		   +0x034 SegmentAllocatorBackTraceIndex : 0
		   +0x036 Reserved         : 0
		   +0x038 UCRSegmentList   : _LIST_ENTRY [ 0x6c4ff0 - 0x6c4ff0 ]
		   +0x040 Flags            : 0x1002
		   +0x044 ForceFlags       : 0
		   +0x048 CompatibilityFlags : 0
		   +0x04c EncodeFlagMask   : 0x100000
		   +0x050 Encoding         : _HEAP_ENTRY
		   +0x058 Interceptor      : 0
		   +0x05c VirtualMemoryThreshold : 0xfe00
		   +0x060 Signature        : 0xeeffeeff
		   +0x064 SegmentReserve   : 0x100000
		   +0x068 SegmentCommit    : 0x2000
		   +0x06c DeCommitFreeBlockThreshold : 0x800
		   +0x070 DeCommitTotalFreeThreshold : 0x2000
		   +0x074 TotalFreeSize    : 0x160
		   +0x078 MaximumAllocationSize : 0x7ffdefff
		   +0x07c ProcessHeapsListIndex : 2
		   +0x07e HeaderValidateLength : 0x248
		   +0x080 HeaderValidateCopy : (null) 
		   +0x084 NextAvailableTagIndex : 0
		   +0x086 MaximumTagIndex  : 0
		   +0x088 TagEntries       : (null) 
		   +0x08c UCRList          : _LIST_ENTRY [ 0x6c4fe8 - 0x6c4fe8 ]
		   +0x094 AlignRound       : 0xf
		   +0x098 AlignMask        : 0xfffffff8
		   +0x09c VirtualAllocdBlocks : _LIST_ENTRY [ 0x6c009c - 0x6c009c ]
		   +0x0a4 SegmentList      : _LIST_ENTRY [ 0x6c0010 - 0x6c0010 ]
		   +0x0ac AllocatorBackTraceIndex : 0
		   +0x0b0 NonDedicatedListLength : 0
		   +0x0b4 BlocksIndex      : 0x006c0260 Void
		   +0x0b8 UCRIndex         : (null) 
		   +0x0bc PseudoTagEntries : (null) 
		   +0x0c0 FreeLists        : _LIST_ENTRY [ 0x6c04e8 - 0x6c45a8 ]
		   +0x0c8 LockVariable     : 0x006c0248 _HEAP_LOCK
		   +0x0cc CommitRoutine    : 0x570e05d9     long  +570e05d9
		   +0x0d0 FrontEndHeap     : 0x00450000 Void
		   +0x0d4 FrontHeapLockCount : 0
		   +0x0d6 FrontEndHeapType : 0x2 ''
		   +0x0d7 RequestedFrontEndHeapType : 0x2 ''
		   +0x0d8 FrontEndHeapUsageData : 0x006c0a70  -> 0
		   +0x0dc FrontEndHeapMaximumIndex : 0x802
		   +0x0de FrontEndHeapStatusBitmap : [257]  ""
		   +0x1e0 Counters         : _HEAP_COUNTERS
		   +0x23c TuningParameters : _HEAP_TUNING_PARAMETERS

		   -- Stuffs interesting for us --

		   0:000> dt nt!_HEAP @@(hHeap) BlocksIndex FrontEndHeap FrontEndHeapType EncodeFlagMask Encoding
		   ntdll!_HEAP
		   +0x04c EncodeFlagMask   : 0x100000
		   +0x050 Encoding         : _HEAP_ENTRY
		   +0x0b4 BlocksIndex      : 0x006c0260 Void
		   +0x0d0 FrontEndHeap     : 0x00450000 Void <- the LFH heap
		   +0x0d6 FrontEndHeapType : 0x2 '' <- Our heap uses the LFH

		   0:000> dt nt!_HEAP 007e0000 BlocksIndex FrontEndHeap FrontEndHeapType EncodeFlagMask Encoding
		   ntdll!_HEAP
		   +0x04c EncodeFlagMask   : 0x100000
		   +0x050 Encoding         : _HEAP_ENTRY
		   +0x0b4 BlocksIndex      : 0x007e0260 Void
		   +0x0d0 FrontEndHeap     : (null) <- No LFH
		   +0x0d6 FrontEndHeapType : 0 '' <- No LFH

		   EncodeFlagMask – A value that is used to determine if a heap chunk header is encoded.
		   This value is initially set to 0x100000 by RtlpCreateHeapEncoding() in RtlCreateHeap()

		   Encoding – Used in an XOR operation to encode the chunk headers, preventing
		   predictable meta-data corruption.

		   BlocksIndex – This is a _HEAP_LIST_LOOKUP structure that is used for a variety of
		   purposes. Due to its importance, it will be discussed in greater detail later in this
		   document.

		   FreeLists – A special linked-list that contains pointers to ALL of the free chunks for this
		   heap. It can almost be thought of as a heap cache, but for chunks of every size (and no
		   single associated bitmap).

		   FrontEndHeapType – An integer is initially set to 0x0, and is subsequently assigned a
		   value of 0x2, indicating the use of a LFH.

		   FrontEndHeap – A pointer to the associated front-end heap. This will either be NULL or
		   a pointer to a _LFH_HEAP structure when running under Windows 7.
	*/
	printf("> hHeap = %p\n", hHeap);
	
	uint32_t x = 2;
	HeapSetInformation(hHeap, HeapCompatibilityInformation, &x, sizeof(uint32_t));
	__debugbreak();

	printf("> Enabling the LFH for size %d..\n", SIZE);
	/*
		0:000> dt _LFH_HEAP 0x00450000 
		ntdll!_LFH_HEAP
		   +0x000 Lock             : _RTL_SRWLOCK
		   +0x004 SubSegmentZones  : _LIST_ENTRY [ 0x6c41a8 - 0x6c41a8 ]
		   +0x00c Heap             : 0x006c0000 Void
		   +0x010 NextSegmentInfoArrayAddress : 0x004508f8 Void
		   +0x014 FirstUncommittedAddress : 0x00451000 Void
		   +0x018 ReservedAddressLimit : 0x0046b000 Void
		   +0x01c SegmentCreate    : 1
		   +0x020 SegmentDelete    : 0
		   +0x024 MinimumCacheDepth : 0
		   +0x028 CacheShiftThreshold : 0
		   +0x02c SizeInCache      : 0
		   +0x030 RunInfo          : _HEAP_BUCKET_RUN_INFO
		   +0x038 UserBlockCache   : [12] _USER_MEMORY_CACHE_ENTRY
		   +0x1b8 MemoryPolicies   : _HEAP_LFH_MEM_POLICIES
		   +0x1bc Buckets          : [129] _HEAP_BUCKET
		   +0x3c0 SegmentInfoArrays : [129] (null) 
		   +0x5c4 AffinitizedInfoArrays : [129] (null) 
		   +0x7c8 SegmentAllocator : (null) 
		   +0x7d0 LocalData        : [1] _HEAP_LOCAL_DATA

		  -- Stuffs interesting

		  0:000> dt _LFH_HEAP 0x00450000 Heap UserBlockCache Buckets LocalData
		  ntdll!_LFH_HEAP
		  +0x00c Heap           : 0x006c0000 Void
		  +0x038 UserBlockCache : [12] _USER_MEMORY_CACHE_ENTRY
		  +0x1bc Buckets        : [129] _HEAP_BUCKET
		  +0x7d0 LocalData      : [1] _HEAP_LOCAL_DATA

	*/
	{
		for (size_t i = 0; i < ENABLE_LFH_N; ++i)
		{
			void *p = HeapAlloc(hHeap, 0, SIZE);
			if (p == nullptr)
				throw std::bad_alloc();

			alloc.push_back(p);
			printf(" . Allocated a block of %d bytes @%p\n", SIZE, p);
			memset(p, 'A', SIZE);
		}

		__debugbreak();

		printf("> First allocation serviced by the LFH..\n");

		VOID *first_lfh_heap_entry = HeapAlloc(hHeap, 0, SIZE);
		memset(first_lfh_heap_entry, '1', SIZE);
		printf("  . Allocated a block of %d bytes @%p\n", SIZE, first_lfh_heap_entry);
		alloc.push_back(first_lfh_heap_entry);

		VOID *second_lfh_heap_entry = HeapAlloc(hHeap, 0, SIZE);
		memset(second_lfh_heap_entry, '2', SIZE);
		printf("  . Allocated a block of %d bytes @%p\n", SIZE, second_lfh_heap_entry);
		alloc.push_back(second_lfh_heap_entry);
	}

	printf("Filling the LFH..\n");

	{
		for (size_t i = 0; i < 26; ++i)
		{
			void *p = HeapAlloc(hHeap, 0, SIZE);
			if (p == nullptr)
				throw std::bad_alloc();

			printf(" . Allocated a block of %d bytes @%p\n", SIZE, p);
			memset(p, i, SIZE);
			alloc.push_back(p);
		}
	}
	
	__debugbreak();
	
	printf("Pushing the LFH's bucket limit..\n");

	{
		for (size_t i = 0; i < 100; ++i)
		{
			void *p = HeapAlloc(hHeap, 0, SIZE);
			if (p == nullptr)
				throw std::bad_alloc();

			printf(" . Allocated a block of %d bytes @%p\n", SIZE, p);
			memset(p, i, SIZE);
			alloc.push_back(p);
		}
	}

	__debugbreak();
	
	printf("Now randomly freeing chunk..\n");
	{
		srand(uint32_t(time(nullptr)));
		while (alloc.size() != 0)
		{
			size_t idx = rand() % alloc.size();
			void *p = alloc.at(idx);
			HeapFree(hHeap, 0, p);
			alloc.erase(
				std::find(
					alloc.begin(), alloc.end(), p
				)
			);
		}
	}
	/*
	{
		#define SIZE_LAST_BUCKET (120)
		for (size_t i = 0; i < ENABLE_LFH_N; ++i)
		{
			alloc[i] = HeapAlloc(hHeap, 0, SIZE_LAST_BUCKET);
			printf(" . Allocated a block of %d bytes @%p\n", SIZE_LAST_BUCKET, alloc[i]);
			memset(alloc[i], 'A', SIZE_LAST_BUCKET);
		}

		printf("> First allocation serviced by the LFH..\n");

		VOID *first_lfh_heap_entry = HeapAlloc(hHeap, 0, SIZE_LAST_BUCKET);
		memset(first_lfh_heap_entry, '3', SIZE_LAST_BUCKET);
		printf("  . Allocated a block of %d bytes @%p\n", SIZE_LAST_BUCKET, first_lfh_heap_entry);

		VOID *second_lfh_heap_entry = HeapAlloc(hHeap, 0, SIZE_LAST_BUCKET);
		memset(second_lfh_heap_entry, '4', SIZE_LAST_BUCKET);
		printf("  . Allocated a block of %d bytes @%p\n", SIZE_LAST_BUCKET, second_lfh_heap_entry);
	}
	*/
	__debugbreak();
	return EXIT_SUCCESS;
}