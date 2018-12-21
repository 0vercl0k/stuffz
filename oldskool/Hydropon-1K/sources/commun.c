#include "commun.h"

int puissance(int a, int b)
{
	int res = 1, i;
	for(i = 0 ; i < b ; i++)
		res *= a;

	return res;
}
