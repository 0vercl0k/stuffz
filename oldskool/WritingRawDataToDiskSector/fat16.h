#ifndef _FAT16_HEADER_
#define _FAT16_HEADER_

/** <Cluster Type> **/
#define CLUSTER_FREE      0x0000
#define CLUSTER_DEFECTIVE 0xFFF7
#define CLUSTER_LAST      0xFFFF
/** </Cluster Type> **/

/** <FAT16 Structures> **/
/** [ Partition Boot Sector ][ FAT1 ][ FAT2 (Duplicate) ][ Root folder ][ Other folders and all files ] **/
#pragma pack(1)
typedef struct _FAT16_BOOT_SECTOR
{
	unsigned char  magic0;                      // 0
	unsigned char  res0;                        // 1
	unsigned char  magic1;                      // 2
	unsigned char  OEMName[8];                  // 3
	unsigned short BytesPerSector;              // 11
	unsigned char  SectorsPerCluster;           // 13
	unsigned short ReservedSectors;             // 14
	unsigned char  FATCount;                    // 16
	unsigned short RootEntries;                 // 17
	unsigned short Sectors;                     // 19
	unsigned char  Media;                       // 21
	unsigned short FATSectors;                  // 22
	unsigned short SectorsPerTrack;             // 24
	unsigned short Heads;                       // 26
	unsigned long  HiddenSectors;               // 28
	unsigned long  SectorsHuge;                 // 32
	unsigned char  Drive;                       // 36
	unsigned char  Res1;                        // 37
	unsigned char  ExtBootSignature;            // 38
	unsigned long  VolumeID;                    // 39
	unsigned char  VolumeLabel[11];             // 43
	unsigned char  SysType[8];                  // 54
	unsigned char  Res2[446];                   // 62
	unsigned long  Signature1;                  // 508
} FAT16_BOOT_SECTOR,
 *PFAT16_BOOT_SECTOR;
/** </FAT16 Structures> **/

/** <FAT16 Functions> **/

int WriteFAT16BootSector(void);

/** </FAT16 Functions> **/
#pragma pack()
#endif