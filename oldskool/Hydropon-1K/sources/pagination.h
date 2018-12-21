#ifndef _PAGINATION
#define _PAGINATION

#define ADDR_DIRECTORY_TABLE_PAGE 0x20000
#define ADDR_TABLE_PAGE0 0x21000
#define ADDR_TABLE_PAGE1 0x22000
#define ADDR_TABLE_PAGE2 0x23000

#define IndiceDansLeRepertoireDePage(x) (x>>22)

//Met en place la pagination
void miseEnPlacePagination(void);


#endif
