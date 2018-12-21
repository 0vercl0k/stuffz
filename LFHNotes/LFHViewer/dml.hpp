#pragma once

//
// Those macro are supposed to make it easier to output data in a descent manner
//

#define DmlNewLine() do \
{                       \
	g_Ext->Dml("\n");   \
} while (false)

#define DmlFieldNameValue(_FieldName, _FieldValueFlag, _FieldValue) do                           \
{                                                                                                \
	g_Ext->Dml("<col fg=\"emphfg\"/>" _FieldName "</col>: " _FieldValueFlag, (_FieldValue));     \
} while(false)

#define DmlVerbFieldNameValue(_FieldName, _FieldValueFlag, _FieldValue) do                                      \
{                                                                                                               \
	g_Ext->DmlVerb("[Verb]<col fg=\"emphfg\"/>" _FieldName "</col>: " _FieldValueFlag "\n", (_FieldValue));     \
} while(false)

#define DmlDoubleFieldNameValue(                                             \
	_FieldName1, _FieldValueFlag1, _FieldValue1,                             \
	_FieldName2, _FieldValueFlag2, _FieldValue2                              \
) do                                                                         \
{                                                                            \
	DmlFieldNameValue(_FieldName1, _FieldValueFlag1, _FieldValue1);          \
	DmlFieldNameValue(" "_FieldName2, _FieldValueFlag2, _FieldValue2);       \
	DmlNewLine();                                                            \
} while (false)
