#pragma once

#include <Windows.h>
#include <engextcpp.hpp>
#include <vector>

class EXT_CLASS : public ExtExtension
{
	public:
		explicit EXT_CLASS() {}

		EXT_COMMAND_METHOD(lfh_);

	private:
};
