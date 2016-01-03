" --------------------------------
" Add our plugin to the path
" --------------------------------
python import sys
python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))

" --------------------------------
"  Function(s)
" --------------------------------
function! BilibiliLiveConnect(chatId)
python << endOfPython
from vim_bilibili_live import connect
connect(vim.eval("a:chatId"))
endOfPython
endfunction

function! BilibiliLiveDisconnect()
python << endOfPython
from vim_bilibili_live import disconnect
disconnect()
endOfPython
endfunction

" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! -nargs=1 BilibiliLiveConnect call BilibiliLiveConnect(<args>)
command! BilibiliLiveDisconnect call BilibiliLiveDisconnect()
