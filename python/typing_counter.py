# Copyright (c) 2010 by fauno <fauno@kiwwwi.com.ar>
#
# Bar item showing typing count. Add 'tc' to a bar.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# 0.1:  initial release
# 0.2:  fixed display bug when buffer changes <weechatter@arcor.de>
#       added cursor position
#       colour of number changes if a specified number of chars are reached
#       reverse counting added
#
# usage:
# add [tc] to your weechat.bar.status.items
#
# config:
# %P = cursor position
# %L = input lenght
# %R = reverse counting from max_chars
# %C = displays how many chars are count over max_chars 
# /set plugins.var.python.typing_counter.format "%P|%L|<%R|%C>"
#
# turns indicator to "warn_colour" when position is reached
# /set plugins.var.python.typing_counter.warn "150"
#
# colour for warn after specified number of chars
# /set plugins.var.python.typing_counter.warn_colour "red"
#
# max number of chars to count reverse
# /set plugins.var.python.typing_counter.max_chars "200"
#
## TODO:
# - buffer whitelist/blacklist
# - max chars per buffer (ie, bar item will turn red when count > 140 for identica buffer)

try:
  import weechat as w

except Exception:
    print "This script must be run under WeeChat."
    print "Get WeeChat now at: http://www.weechat.org/"
    quit()

SCRIPT_NAME    = "typing_counter"
SCRIPT_AUTHOR  = "fauno <fauno@kiwwwi.com.ar>"
SCRIPT_VERSION = "0.2"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC    = "Bar item showing typing count and cursor position. Add 'tc' to a bar."

tc_input_text   = ''
laenge          = 0
cursor_pos      = 1
format          = "[%P|%L|<%R|%C>]"
warn            = "140"
warn_colour     = "red"
max_chars       = "200"
count_over      = "0"

def tc_bar_item_update (data, modifier, modifier_data): #data, modifier, modifier_data, string
    '''Updates bar item'''
    global laenge, cursor_pos, tc_input_text

    current_buffer = w.current_buffer()
    laenge = w.buffer_get_integer(current_buffer,'input_length')
    cursor_pos = w.buffer_get_integer(current_buffer,'input_pos') + 1
    w.bar_item_update('tc')
    return w.WEECHAT_RC_OK

def tc_bar_item (data, item, window):
    '''Item constructor'''
    global laenge, cursor_pos, tc_input_text, count_over

    # reverse check for max_chars
    reverse_chars = (int(max_chars) - laenge)
    if reverse_chars == 0:
        reverse_chars = "%s" % ("0")
        count_over = "0"
    else:
        if reverse_chars < 0:
            count_over = "%s%s%s" % (w.color(warn_colour),str(reverse_chars*-1), w.color('default'))
            reverse_chars = "%s" % ("0")
        else:
            reverse_chars = str(reverse_chars)
    out_format = format
    if laenge >= int(warn):
        laenge_warn = "%s%s%s" % (w.color(warn_colour), str(laenge), w.color('default'))
        out_format = out_format.replace('%L', laenge_warn)
    else:
        out_format = out_format.replace('%L', str(laenge))

    out_format = out_format.replace('%P', str(cursor_pos))
    out_format = out_format.replace('%R', reverse_chars)
    out_format = out_format.replace('%C', count_over)
    tc_input_text = out_format
    return tc_input_text

if __name__ == "__main__":
    if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                  SCRIPT_LICENSE, SCRIPT_DESC,
                  "", ""):
        if not w.config_get_plugin('format'): 
            w.config_set_plugin('format', format)
        format = w.config_get_plugin('format')
        if not w.config_get_plugin('warn'): 
            w.config_set_plugin('warn', warn)
        warn = w.config_get_plugin('max_chars')
        if not w.config_get_plugin('max_chars'): 
            w.config_set_plugin('max_chars', max_chars)
        warn = w.config_get_plugin('warn')
        if not w.config_get_plugin('warn_colour'): 
            w.config_set_plugin('warn_colour', warn_colour)
        warn_colour = w.config_get_plugin('warn_colour')

        w.hook_signal('input_text_changed', 'tc_bar_item_update', '')
        w.hook_signal('input_text_cursor_moved','tc_bar_item_update','')
        w.hook_signal('buffer_switch','tc_bar_item_update','')
        w.bar_item_new('tc', 'tc_bar_item', '')