#define _CRT_SECURE_NO_WARNINGS
#include "main.hpp"
#include "dml.hpp"

#include <array>
#include <ctime>

//
// Debugger Engine Overview
// http://msdn.microsoft.com/en-us/library/windows/hardware/ff540534(v=vs.85).aspx
//

#define LFH_FREE (0x80)

EXT_DECLARE_GLOBALS();

/// .load D:\Codes\LFHNotes\Debug\LFHViewer.dll

// Return all the heaps available for your process
std::vector<ULONG64>
GetProcessHeaps(
	VOID
)

/*++
	Routine Description:

		Displays interrupt descriptor table.
	
	Return Value:
	
		BOOL
	
	Environment:
	
		Kernel mode.

	Note:

		Supports only the x86-based platform.
--*/

{
	ExtRemoteTyped peb("(nt!_PEB*)@$peb");
	std::vector<ULONG64> heaps;

	//
	// Enumerates all the available heaps for the current process
	//
	
	DmlVerbFieldNameValue("ProcessHeaps value", "%p", peb.Field("ProcessHeaps").GetPtr());
	DmlVerbFieldNameValue("NumberOfHeap value", "%d", peb.Field("NumberOfHeaps").GetUlong());

	for (size_t i = 0; i < peb.Field("NumberOfHeaps").GetUlong(); ++i)
		heaps.emplace_back(
			peb.Field("ProcessHeaps").ArrayElement(i).GetPtr()
		);

	return heaps;
}


BOOL
IsLFHEnabled(
	_In_ ULONG64 HeapAddress
)

/*++
	Routine Description:

		Is the LFH enabled for this heap?
	
	Return Value:
	
		BOOL
	
	Note:

--*/

{
	ExtRemoteTyped Heap("(nt!_HEAP*)@$extin", HeapAddress);

	//
	// FrontEndHeap is supposed to be a pointer to a _LFH_HEAP structure,
	// so if it's NULL it means the heap doesn't use the LFH
	//
	
	return Heap.Field("FrontEndHeap").GetPtr() != NULL &&
		Heap.Field("FrontEndHeapType").GetUchar() != 0;
}

struct Chunk {
	bool free;
	uint64_t address;
	std::string content;
	Chunk(uint64_t address, std::string content, bool free) : address{ address }, content{ content }, free{ free } {}
	void json(FILE *f)
	{
		fprintf(
			f,
			"{ \"address\" : %lld, \"content\" : \"%s\", \"state\" : \"%s\" }",
			address, content.c_str(), (free ? "free" : "busy")
			);
	}
};

struct Bucket {
	uint64_t size;
	std::vector<Chunk> chunks;
	void json(FILE *f)
	{
		fprintf(f, "{ \"size\" : %lld, \"chunks\" : [", size);
		for (auto &chunk : chunks)
		{
			chunk.json(f);
			if (&chunk != &(chunks.back()))
				fprintf(f, ",");
		}
		fprintf(f, "  ]}");
	}
};

struct LFHeap {
	LFHeap() : address{ 0 } {}
	uint64_t address;
	std::vector<Bucket> buckets;
	void json(FILE *f)
	{
		fprintf(f, "{ \"address\" : %lld, \"buckets\" : [", address);
		for (auto &bucket : buckets)
		{
			bucket.json(f);
			if (&bucket != &(buckets.back()))
				fprintf(f, ",");
		}
		fprintf(f, "]}");
	}
};

// http://illmatics.com/Understanding_the_LFH.pdf
EXT_COMMAND(lfh_, "Sample extension command", "")
{
	//
	// You can remove that line if you don't want all the
	// DmlVerb/crap messages displayed.
	//
	// g_Ext->m_Client->SetOutputMask(DEBUG_OUTPUT_NORMAL | DEBUG_OUTPUT_VERBOSE | DEBUG_OUTPUT_WARNING | DEBUG_OUTPUT_ERROR);
	
	std::vector<LFHeap> LFHHeaps;

	//
	// Listing the LFH enabled heaps
	//

	ULONG64 RtlpLFHKeyAddress;
	if (g_Ext->m_Symbols->GetOffsetByName("ntdll!RtlpLFHKey", &RtlpLFHKeyAddress) != S_OK)
		return;

	ULONG32 RtlpLFHKey;
	ExtRemoteData RtlpLFHKeyExt(RtlpLFHKeyAddress, sizeof(void*));
	RtlpLFHKey = RtlpLFHKeyExt.GetUlong();

	for (ULONG64 HeapAddress : GetProcessHeaps())
	{
		g_Ext->Dml("<col fg=\"emphfg\"/>Heap Address</col>: <exec cmd=\"dx (nt!_HEAP*)0x%p\">%p</exec> ", HeapAddress, HeapAddress);
		g_Ext->Dml("<col fg=\"emphfg\"/>LFH Address</col>: ");

		//
		// If the LFH is enabled let's output some helper exec command
		//

		if (IsLFHEnabled(HeapAddress))
		{
			LFHeap CurrentLFH;
			CurrentLFH.address = HeapAddress;

			ExtRemoteTyped Heap("(nt!_HEAP*)@$extin", HeapAddress);
			ULONG64 LFHAddress = Heap.Field("FrontEndHeap").GetPtr();
			g_Ext->Dml("<exec cmd=\"dx (nt!_LFH_HEAP*)0x%p\">%p</exec>\n", LFHAddress, LFHAddress);

			//
			// Check which buckets for which sizes exist
			//

			ExtRemoteTyped LFH("(nt!_LFH_HEAP*)@$extin", LFHAddress);

			//
			// Keep in mind the LFH has 128 buckets; servicing allocations with 8 bytes aligned sizes that are smaller than XXX
			//

			//XXX:FrontEndHeapUsageData
			for (SIZE_T BucketId = 0; BucketId < 128; ++BucketId)
			{
				ULONG64 LocalSegmentInfoAddress = LFH.Field("SegmentInfoArrays").ArrayElement(BucketId).GetPtr();
				if (LocalSegmentInfoAddress == 0)
					continue;

				ExtRemoteTyped LocalSegmentInfo("(nt!_HEAP_LOCAL_SEGMENT_INFO*)@$extin", LocalSegmentInfoAddress);

				//
				// A bucket can have more than one SubSegment, let's iterate over them
				//

				ULONG32 SubSegmentCounts = LocalSegmentInfo.Field("Counters").Field("SubSegmentCounts").GetUlong();

				//
				// Keeping the ActiveSubSegment address somewhere, so that we can tag this one in a special way
				//

				ULONG64 ActiveSubSegmentAddress = LocalSegmentInfo.Field("ActiveSubsegment").GetPtr();

				/// WoW64 ntdll.dll v10.0.10586.20
				/// int __fastcall RtlpLowFragHeapAllocateFromZone(_LFH_HEAP *LFH, int LocalIndex)
				/// {
				/// 	[...]
				/// 	Zone = LFH->LocalData[LocalIndex].CrtZone.ListEntry.Flink;
				/// 	if (Zone)
				/// 	{
				/// 		NewNextIndex = _InterlockedExchangeAdd(Zone->NextIndex, 1u);
				/// 		if ((unsigned int)NewNextIndex < 0x19)
				/// 			return  (sizeof(ntdll!_HEAP_SUBSEGMENT) * NewNextIndex) + Zone + sizeof(ntdll!_LFH_BLOCK_ZONE) + 4;
					
				// XXX: We might also want to iter over every Zone in the linkedlist

				ULONG64 CrtZoneAddress = LocalSegmentInfo.Field("LocalData").Field("CrtZone").GetPtr();
				if (CrtZoneAddress == 0)
				{
					g_Ext->Dml("No CrtZone available, skipping..\n");
					continue;
				}

				ExtRemoteTyped CrtZone("(nt!_LFH_BLOCK_ZONE*)@$extin", CrtZoneAddress);

				g_Ext->Dml(
					" <col fg=\"emphfg\"/><exec cmd=\"dx (nt!_HEAP_LOCAL_SEGMENT_INFO*)0x%p\">Segment %.3d</exec></col> (Total BlockCount: %d, SubSegmentCounts: %d)\n",
					LocalSegmentInfoAddress,
					LocalSegmentInfo.Field("BucketIndex").GetUshort(),
					LocalSegmentInfo.Field("Counters").Field("TotalBlocks").GetUlong(),
					SubSegmentCounts
				);

				Bucket CurrentBucket;

				for (
					SIZE_T ZoneIdx = 0, SubSegmentParsed = 0; 
					(ZoneIdx < CrtZone.Field("NextIndex").GetUlong()) && (SubSegmentParsed < SubSegmentCounts);
					++ZoneIdx
				)
				{
					ULONG64 SubSegmentAddress = (GetTypeSize("nt!_HEAP_SUBSEGMENT") * ZoneIdx) + (CrtZoneAddress + GetTypeSize("nt!_LFH_BLOCK_ZONE") + 4); // XXX: Check X64 -- round to handle both x86/64?
					ExtRemoteTyped SubSegment("(nt!_HEAP_SUBSEGMENT*)@$extin", SubSegmentAddress);
					
					//
					// Now make sure the Segment is not freed and or in good shape - the best way I found to do that
					// is to make sure its BucketIndex is the one we expect
					//
						
					if (SubSegment.Field("LocalInfo").Field("BucketIndex").GetUshort() != BucketId)
						continue;

					BOOLEAN IsSubSegmentActive = (ActiveSubSegmentAddress == SubSegmentAddress);

					//
					// The size are expressed in blocks and one block is 8 bytes long
					//

					USHORT BlockSize = SubSegment.Field("BlockSize").GetUshort() * 8;
					USHORT BlockCount = SubSegment.Field("BlockCount").GetUshort();

					ULONG64 UserBlocksAddress = SubSegment.Field("UserBlocks").GetPtr();
					if (UserBlocksAddress == 0)
					{
						g_Ext->Dml("UserBlocksAddress is null, weird.\n");
						__debugbreak();
					}
					ExtRemoteTyped UserBlocks("(nt!_HEAP_USERDATA_HEADER*)@$extin", UserBlocksAddress);

					g_Ext->Dml(
						"  <exec cmd = \"dx (nt!_HEAP_SUBSEGMENT*)0x%p\">SubSegment</exec> %d Blocks of %d bytes, GuardPagePresent: <b>%d</b>, Active: %s\n",
						ActiveSubSegmentAddress,
						BlockCount,
						BlockSize,
						UserBlocks.Field("GuardPagePresent").GetUchar(),
						(IsSubSegmentActive ? "<b>yes</b>" : "no")
					);
					
					//
					// If we haven't set the size on the CurrentBucket, then do it!
					//
					
					if (CurrentBucket.size != BlockSize)
						CurrentBucket.size = BlockSize;

					for (SIZE_T j = 0; j < BlockCount; ++j)
					{
						USHORT FirstAllocationOffset = USHORT(RtlpLFHKey ^ LFHAddress ^ UserBlocksAddress ^ UserBlocks.Field("EncodedOffsets").Field("FirstAllocationOffset").GetUshort());
						ULONG64 HeapEntryAddress = UserBlocksAddress + FirstAllocationOffset + (BlockSize * j);
						ExtRemoteTyped HeapEntry("(nt!_HEAP_ENTRY*)@$extin", HeapEntryAddress);

						//
						// Don't forget there is a 8 bytes long header - which the user does not see
						//

						ULONG64 UserBlockAddress = HeapEntryAddress + GetTypeSize("nt!_HEAP_ENTRY");
						USHORT UserBlockSize = USHORT(BlockSize - GetTypeSize("nt!_HEAP_ENTRY"));
						BOOLEAN IsFreeBlock = HeapEntry.Field("UnusedBytes").GetUchar() == LFH_FREE;
						
						{
							std::array<uint8_t, 8> data;
							g_Ext->m_Data->ReadVirtual(UserBlockAddress, data.data(), data.size(), nullptr);
							std::string hex;
							for (size_t i = 0; i < data.size(); ++i)
							{
								char byte[3] { };
								sprintf(byte, "%.2x", data.at(i));
								hex.append(byte);
								if((i + 1) != data.size())
									hex += ' ';
							}
							
							CurrentBucket.chunks.emplace_back(UserBlockAddress, hex, (IsFreeBlock == TRUE ? true : false));
						}

						g_Ext->Dml(
							"   <col fg=\"emphfg\"><exec cmd=\"dx (nt!_HEAP_ENTRY*)0x%p\">%p</exec></col> - <exec cmd=\"db %p l0n%d\">User Address: %p</exec> <b><col fg=\"%s\">%s</col></b>\n",
							HeapEntryAddress,
							HeapEntryAddress,
							UserBlockAddress,
							UserBlockSize,
							UserBlockAddress,
							(IsFreeBlock ? "normfg" : "changed"),
							(IsFreeBlock ? "FREE" : "BUSY")
						);
					}

					SubSegmentParsed++;
				}
				CurrentLFH.buckets.push_back(CurrentBucket);
			}
			LFHHeaps.push_back(CurrentLFH);
		}
		else
			g_Ext->Dml("Off");

		g_Ext->Dml("\n");
	}
	
	static uint64_t njson = 0;
	#define FORMAT "D:\\Codes\\LFHNotes\\jsons\\test.%lld.json"
	size_t SizeNeeded = _scprintf(FORMAT, njson);
	std::vector<char> Path(SizeNeeded + 1, 0);
	
	sprintf(Path.data(), FORMAT, njson);

	FILE *f = fopen(Path.data(), "w");
	fprintf(f, "{ \"LFHs\" : [");
	for (auto &lfh : LFHHeaps)
	{
		lfh.json(f);
		if(&lfh != &(LFHHeaps.back()))
			fprintf(f, ",");
	}
	fprintf(f, "]}");
	fclose(f);
	njson++;
}
