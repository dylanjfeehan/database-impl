---
tags:
  - part-0-filesystem
---
# C++ Reference Code for PagedFile Handle
This class is initiated and then unixfd is populated by passing a reference to this object to the manager Open function. The population of the unixfd file descriptor is what gives this class its functionality
## State
 - `PF_BufferMgr *pBufferMgr;                      // pointer to buffer manager`
 - `PF_FileHdr hdr;                                // file header`
 - `int bFileOpen;                                 // file open flag`
 - `int bHdrChanged;                               // dirty flag for file hdr`
 - `int unixfd;                                    // OS file descriptor`

## Functions
The most important functionality of the PagedFile handle is the ability to allocate pages, get pages based on page number, and dispose pages.
### Allocate Page
``` C++
// AllocatePage
//
// Desc: Allocate a new page in the file (may get a page which was
//       previously disposed)
//       The file handle must refer to an open file
// Out:  pageHandle - becomes a handle to the newly-allocated page
//                    this function modifies local var's in pageHandle
// Ret:  PF return code
//
RC PF_FileHandle::AllocatePage(PF_PageHandle &pageHandle)
{
   int     rc;               // return code
   int     pageNum;          // new-page number
   char    *pPageBuf;        // address of page in buffer pool

   // File must be open
   if (!bFileOpen)
      return (PF_CLOSEDFILE);

   // If the free list isn't empty...
   if (hdr.firstFree != PF_PAGE_LIST_END) {
      pageNum = hdr.firstFree;

      // Get the first free page into the buffer
      if ((rc = pBufferMgr->GetPage(unixfd,
            pageNum,
            &pPageBuf)))
         return (rc);

      // Set the first free page to the next page on the free list
      hdr.firstFree = ((PF_PageHdr*)pPageBuf)->nextFree;
   }
   else {

      // The free list is empty...
      pageNum = hdr.numPages;

      // Allocate a new page in the file
      if ((rc = pBufferMgr->AllocatePage(unixfd,
            pageNum,
            &pPageBuf)))
         return (rc);

      // Increment the number of pages for this file
      hdr.numPages++;
   }

   // Mark the header as changed
   bHdrChanged = TRUE;

   // Mark this page as used
   ((PF_PageHdr *)pPageBuf)->nextFree = PF_PAGE_USED;

   // Zero out the page data
   memset(pPageBuf + sizeof(PF_PageHdr), 0, PF_PAGE_SIZE);

   // Mark the page dirty because we changed the next pointer
   if ((rc = MarkDirty(pageNum)))
      return (rc);

   // Set the pageHandle local variables
   pageHandle.pageNum = pageNum;
   pageHandle.pPageData = pPageBuf + sizeof(PF_PageHdr);

   // Return ok
   return (0);
}
```
