# telescope.js

telescope.js is a [JavaScript](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/javascript-debugger-scripting) debugger extension  for WinDbg which mirror the `!telescope` command from [GEF](https://github.com/hugsy/gef).

## Usage
Run `.scriptload telescope.js` to load the script. You can invoke the telescope feature with `!telescope <addr>` or programatically via `dx @$createchain(<addr>)`.

## Examples
