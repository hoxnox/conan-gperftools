#include <gperftools/malloc_extension.h>
#include <iostream>

int main(int argc, char* argv[])
{
	size_t value;
	MallocExtension::instance()->GetNumericProperty("generic.heap_size", &value);
	std::cout << value << std::endl;
	return 0;
}

