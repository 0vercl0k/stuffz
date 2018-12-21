#include "fat16.h"
/** <FAT16 Functions> **/

int WriteFAT16BootSector(void)
{
	FAT_BOOT_SECTOR fatBootSector = {0};
	BootSector.BytesPerSector = DiskGeometry->BytesPerSector;
	BootSector.SectorsPerCluster = ClusterSize / BootSector.BytesPerSector;
	BootSector.ReservedSectors = 1;
	BootSector.FATCount = 2;
	BootSector.RootEntries = 512;
	BootSector.Sectors = (SectorCount < 0x10000) ? (unsigned short)SectorCount : 0;
	BootSector.Media = 0xf8;
	BootSector.FATSectors = 0;  /* Set later. See below. */
	BootSector.SectorsPerTrack = DiskGeometry->SectorsPerTrack;
	BootSector.Heads = DiskGeometry->TracksPerCylinder;
	BootSector.HiddenSectors = PartitionInfo->HiddenSectors;
	BootSector.SectorsHuge = (SectorCount >= 0x10000) ? (unsigned long)SectorCount : 0;
	BootSector.Drive = 0xff; /* No BIOS boot drive available */
	BootSector.ExtBootSignature = 0x29;
	BootSector.VolumeID = CalcVolumeSerialNumber();
	return 1;
}

/** </FAT16 Functions> **/