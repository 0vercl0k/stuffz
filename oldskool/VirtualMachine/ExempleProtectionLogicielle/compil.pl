use strict;
use warnings;

my @code , my $i = 0 ;
my %registre = ( eax => '\x00' , ebx => '\x01' , ecx => '\x02' , edx => '\x03' );
my %instru   = ( inc_reg => '\x12' , push_dwd => '\x20' , push_reg => '\x21' , pop_reg => '\x13' ,
		         mov_reg_reg => '\x14' , mov_reg_imm => '\x15' , mov_reg_ptrimm => '\x16' , mov_ptrreg_reg => '\x17' , mov_ptrreg_imm => '\x18', mov_reg_ptrreg => '\x19' ,
				 invoke4args => '\x23' , invoke3args => '\x22',
				 jneimm => '\x24',
				 exit_ => '\x25' ,
				 cmp_reg_reg => '\x26');

print "Compil 0vercl0k's instructions.\n";
die("Usage : compil.pl <fichier>") if(@ARGV == 0);

open( FILE , '<'.$ARGV[0] );
@code = <FILE>;
chomp(@code);
close(FILE);

$i = 0;
print 'char code[] = "';
foreach my $tmp (@code)
{
	my @part = split(/ / , $tmp);
	if( (my $opcode = &validInstructions(@part)) ne '' )	{ print $opcode; }
	else { print "Instruction mal formaté.\n\n" ; exit; }
}
print "\";\n";



sub validInstructions()
{
	my $cmd = '';
	my ($instru , $dest , $src ) = @_;
	
	if($instru eq 'inc') #instruction inc
	{
		if( $dest =~ /^(e[a-d]x)$/ )
		{
			$cmd = $instru{'inc_reg'}.$registre{"$1"};
			return $cmd;
		}
		return '';
	}
	
	if($instru eq 'push')
	{
		if( $dest =~ /^([0-9]{8})h$/ ) #push 11223344h
		{
			
			$cmd = $instru{'push_dwd'}.'\x'.substr($1 , 6 , 2).'\x'.substr ($1 , 4 , 2).'\x'.substr($1 , 2 , 2).'\x'.substr($1 , 0 , 2);
			return $cmd;
		}
		
		if( $dest =~ /^(e[a-d]x)$/ )
		{
			$cmd = $instru{'push_reg'}.$registre{"$1"};
			return $cmd;
		}
		return '';
	}
	
	if($instru eq 'pop')
	{
		if($dest =~ /^(e[a-d]x)$/)
		{
			$cmd = $instru{'pop_reg'}.$registre{"$1"};
			return $cmd;
		}
		return '';
	}
	
	if($instru eq 'mov')
	{
		if($dest =~ /^(e[a-d]x),(e[a-d]x)$/)
		{
			$cmd = $instru{'mov_reg_reg'}.$registre{"$1"}.$registre{"$2"};
			return $cmd;
		}
		
		if($dest =~ /^(e[a-d]x),([0-9a-f]{8})h$/i)
		{
			$cmd = $instru{'mov_reg_imm'}.$registre{"$1"}.'\x'.substr($2 , 6 , 2).'\x'.substr ($2 , 4 , 2).'\x'.substr($2 , 2 , 2).'\x'.substr($2 , 0 , 2);
			return $cmd;
		}
		
		if($dest =~ /^(e[a-d]x),\[([0-9a-f]{8})h\]$/i)
		{
			$cmd = $instru{'mov_reg_ptrimm'}.$registre{"$1"}.'\x'.substr($2 , 6 , 2).'\x'.substr ($2 , 4 , 2).'\x'.substr($2 , 2 , 2).'\x'.substr($2 , 0 , 2);
			return $cmd;
		}
		
		if($dest =~ /^\[(e[a-d]x)\],(e[a-d]x)$/)
		{
			$cmd = $instru{'mov_ptrreg_reg'}.$registre{"$1"}.$registre{"$2"};
			return $cmd;
		}
		
		if($dest =~ /^\[(e[a-d]x)\],([0-9a-f]{8})h$/i)
		{
			$cmd = $instru{'mov_ptrreg_imm'}.$registre{"$1"}.'\x'.substr($2 , 6 , 2).'\x'.substr ($2 , 4 , 2).'\x'.substr($2 , 2 , 2).'\x'.substr($2 , 0 , 2);
			return $cmd;
		}
		
		if($dest =~ /^(e[a-d]x),\[(e[a-d]x)\]$/)
		{
			$cmd = $instru{'mov_reg_ptrreg'}.$registre{"$1"}.$registre{"$2"};
			return $cmd;
		}
		
		return '';
	}
	
	if($instru eq 'invoke')
	{
		if($dest =~ /^([0-9a-f]{8})h,([0-9a-f]{8})h,([0-9a-f]{8})h,([0-9a-f]{8})h,([0-9a-f]{8})h$/i)
		{
			$cmd  = $instru{'invoke4args'}.'\x'.substr($1 , 6 , 2).'\x'.substr ($1 , 4 , 2).'\x'.substr($1 , 2 , 2).'\x'.substr($1 , 0 , 2);
			$cmd .= '\x'.substr($2 , 6 , 2).'\x'.substr ($2 , 4 , 2).'\x'.substr($2 , 2 , 2).'\x'.substr($2 , 0 , 2);
			$cmd .= '\x'.substr($3 , 6 , 2).'\x'.substr ($3 , 4 , 2).'\x'.substr($3 , 2 , 2).'\x'.substr($3 , 0 , 2);
			$cmd .= '\x'.substr($4 , 6 , 2).'\x'.substr ($4 , 4 , 2).'\x'.substr($4 , 2 , 2).'\x'.substr($4 , 0 , 2);
			$cmd .= '\x'.substr($5 , 6 , 2).'\x'.substr ($5 , 4 , 2).'\x'.substr($5 , 2 , 2).'\x'.substr($5 , 0 , 2);
			return $cmd;
		}
		
		if($dest =~ /^([0-9a-f]{8})h,([0-9a-f]{8})h,([0-9a-f]{8})h,([0-9a-f]{8})h$/i)
		{
			$cmd  = $instru{'invoke3args'}.'\x'.substr($1 , 6 , 2).'\x'.substr ($1 , 4 , 2).'\x'.substr($1 , 2 , 2).'\x'.substr($1 , 0 , 2);
			$cmd .= '\x'.substr($2 , 6 , 2).'\x'.substr ($2 , 4 , 2).'\x'.substr($2 , 2 , 2).'\x'.substr($2 , 0 , 2);
			$cmd .= '\x'.substr($3 , 6 , 2).'\x'.substr ($3 , 4 , 2).'\x'.substr($3 , 2 , 2).'\x'.substr($3 , 0 , 2);
			$cmd .= '\x'.substr($4 , 6 , 2).'\x'.substr ($4 , 4 , 2).'\x'.substr($4 , 2 , 2).'\x'.substr($4 , 0 , 2);
			return $cmd;
		}
		return '';
	}
	
	if($instru eq 'jne')
	{
		if($dest =~ /^([0-9a-f]{8})h$/i)
		{
			$cmd = $instru{'jneimm'}.'\x'.substr($1 , 6 , 2).'\x'.substr ($1 , 4 , 2).'\x'.substr($1 , 2 , 2).'\x'.substr($1 , 0 , 2);
			return $cmd;
		}
		return '';
	}
	
	if($instru eq 'exit')
	{
		$cmd = $instru{'exit_'};
		return $cmd;
	}
	
	if($instru eq 'cmp')
	{
		if($dest =~ /^(e[a-d]x),(e[a-d]x)$/)
		{
			$cmd = $instru{'cmp_reg_reg'}.$registre{"$1"}.$registre{"$2"};
			return $cmd;
		}
		return '';
	}
	return '';
}