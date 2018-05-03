#include <string.h>
#include <errno.h>
#include <stdio.h>

#include <http_parser.h>

int
main(int argc, char **argv)
{
	unsigned long version = http_parser_version();
	unsigned major = (version >> 16) & 255;
	unsigned minor = (version >> 8) & 255;
	unsigned patch = version & 255;
	printf("http_parser v%u.%u.%u\n", major, minor, patch);
	printf("done\n");
	return 0;
}
