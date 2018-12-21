#Pour 0vercl0k.blogspot.com <> 0vercl0k.fr par 0vercl0k.
use strict;
use warnings;

my ($tab,@tab,$i,$push,$count);

if(@ARGV == 0)
{
	print("./push.pl <string>.\n\n");
	exit;
}


@tab = split(//,$ARGV[0]);
if(($count = scalar(@tab)) % 4 != 0)
{
	while(($count % 4) != 0)
	{
		$tab[$count] = "\x00";
		$count++;
	}
}

print("xor eax,eax\npush eax\n");

for( $i = (scalar(@tab)-1) ; $i >= 0 ; $i-- )
{
	$push .= unpack("H*",$tab[$i]);
	if(  ($i%4) == 0)
	{
		print("push ".$push."h\n");
		$push = '';
	}
}