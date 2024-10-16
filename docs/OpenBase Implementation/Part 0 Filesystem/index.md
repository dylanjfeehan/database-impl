---
tags:
  - part-0-filesystem
---

# Overview
The first step will be to build an interface that allows us to interface with files in our filesystem at the page granularity. We will use a reference implementation of C++ to guide us through this process. This provides a gentler introductionn to Go since we don't have to design this from scratch.

## PagedFile Interface
The three main parts of the filesystem interface we're building are the PagedFile Manager, the PagedFile handle, and the page handle. 
### PagedFile Manager
The PagedFile manager allows for typical lifecycle operations of creating, destroying, opening, and closing PagedFiles. The PagedFile manager can provide clients with PagedFile handles
### PagedFile handles
PagedFile handles can be used to allocate / deallocated file pages, search through pages, and do management modifications to pages like pinning and marking dirty.
### Page handles
Page handle provides access to the contents of a given page

## C++ Reference Code

## Go Implementation