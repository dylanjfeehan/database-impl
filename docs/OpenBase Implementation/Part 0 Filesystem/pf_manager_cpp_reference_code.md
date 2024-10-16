---
tags:
  - part-0-filesystem
---
# C++ Reference Code for PagedFile Manager
## State
This class stores no state
## Functions
The most important functionnality of the PagedFile manager is **creating** and **opening** files.
### Creating a PagedFile
``` C++
// Desc: Create a new PF file named fileName
// In:   fileName - name of file to create
// Ret:  PF return code
//
RC PF_Manager::CreateFile (const char *fileName)
{
   int fd;		// unix file descriptor
   int numBytes;		// return code form write syscall

   // Create file for exclusive use (1)
   if ((fd = open(fileName, // (2)!
#ifdef PC
         O_BINARY |
#endif
         O_CREAT | O_EXCL | O_WRONLY,
         CREATION_MASK)) < 0)
      return (PF_UNIX);

   // Initialize the file header: must reserve FileHdrSize bytes in memory
   // though the actual size of FileHdr is smaller
   char hdrBuf[PF_FILE_HDR_SIZE];

   // So that Purify doesn't complain
   memset(hdrBuf, 0, PF_FILE_HDR_SIZE);

   PF_FileHdr *hdr = (PF_FileHdr*)hdrBuf;
   hdr->firstFree = PF_PAGE_LIST_END;
   hdr->numPages = 0;

   // Write header to file
   if((numBytes = write(fd, hdrBuf, PF_FILE_HDR_SIZE))
         != PF_FILE_HDR_SIZE) {

      // Error while writing: close and remove file
      close(fd);
      unlink(fileName);

      // Return an error
      if(numBytes < 0)
         return (PF_UNIX);
      else
         return (PF_HDRWRITE);
   }

   // Close file
   if(close(fd) < 0)
      return (PF_UNIX);

   // Return ok
   return (0);
}
```

1.  the `open` syscall is capable of opening files or creating them if they do not yet exist
2.  assignments are expressions in C++. The value of the expression is the value stored in the left operand after the assignment has taken place

## Opening a PagedFile
A client has a PF_Manager object. The client creates a PF_FileHandle object. The client calls PF_Manager::OpenFile and passes along a reference to their
 FileHandle object. After this function completes, if successful, the FileHandle object will now have an initialized fileDescriptor.
``` C++
// Desc: Open the paged file whose name is "fileName".  It is possible to open
//       a file more than once, however, it will be treated as 2 separate files
//       (different file descriptors; different buffers).  Thus, opening a file
//       more than once for writing may corrupt the file, and can, in certain
//       circumstances, crash the PF layer. Note that even if only one instance
//       of a file is for writing, problems may occur because some writes may
//       not be seen by a reader of another instance of the file.
// In:   fileName - name of file to open
// Out:  fileHandle - refer to the open file
//                    this function modifies local var's in fileHandle
//       to point to the file data in the file table, and to point to the
//       buffer manager object
// Ret:  PF_FILEOPEN or other PF return code
//
RC PF_Manager::OpenFile (const char *fileName, PF_FileHandle &fileHandle) {
    // return code
   int rc; // (1)!

   // Ensure file is not already open
   if (fileHandle.bFileOpen)
      return (PF_FILEOPEN);

   // Open the file
   if ((fileHandle.unixfd = open(fileName, // (2)!
#ifdef PC
         O_BINARY | 
#endif
         O_RDWR)) < 0)
      return (PF_UNIX);

   // Read the file header
   {
      int numBytes = read(fileHandle.unixfd, (char *)&fileHandle.hdr,
            sizeof(PF_FileHdr));
      if (numBytes != sizeof(PF_FileHdr)) {
         rc = (numBytes < 0) ? PF_UNIX : PF_HDRREAD;
         goto err; // (3)!
      }
   }

   // Set file header to be not changed
   fileHandle.bHdrChanged = FALSE;

   // Set local variables in file handle object to refer to open file
   fileHandle.pBufferMgr = pBufferMgr;
   fileHandle.bFileOpen = TRUE;

   // Return ok
   return 0;

err:
   // Close file
   close(fileHandle.unixfd);
   fileHandle.bFileOpen = FALSE;

   // Return error
   return (rc);
}
```

1.  return code
2.  assignments are expressions in C++. The value of the expression is the value stored in the left operand after the assignment has taken place
3.  the goto statement transfers control to the location specified by label